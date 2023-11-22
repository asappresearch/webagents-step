from webactions_lm.policy.policy import Policy
from webactions_lm.utils.llm import add_latest_state_to_prompt

VALID_SKILL_TYPES = ["fill_text", "choose_date", "find_and_click_search_link", "find_and_click_tab_link", "select_flight", "find_commit", "search_issue", "find_directions", "search_nearest_place", "click_checkboxes", "process_email"]
VALID_ACTION_TYPES = ["click", "type", "stop", "scroll"]

class LowLevelSkillPolicy(Policy):
    def __init__(self, env, call_llm_fn, prompt_library, skill_type, max_iters=5, debug=False, verbose=0):
        self.env = env
        self.call_llm_fn = call_llm_fn
        self.prompt_library = prompt_library
        self.skill_type = skill_type

        self.base_prompt = getattr(self.prompt_library, skill_type)
        self.prev_actions = []
        self.debug = debug
        self.verbose = verbose
        self.max_iters = max_iters
        

    def _get_llm_action(self, obs, objective):
        browser_content = obs

        prompt = add_latest_state_to_prompt(prompt=self.base_prompt, context=objective,
                                            url=self.env.url, browser_content=browser_content,
                                            prev_actions="\n".join(self.prev_actions))
        action, reason = self.call_llm_fn(prompt)
        
        if "\n" in action:
            action = action.split("\n", 1)[0]

        if self.verbose > 0:
            if self.verbose > 1:
                print(browser_content)        
            print(f"\n Context: {objective}")
            prev_actions="\n".join(self.prev_actions)
            print(f"\n Previous Actions: {prev_actions}")
            print(f"\n Reason: {reason}")
            print(f"\n Action: {action}")
            print(f"Low level sill being executed: {self.skill_type}")
        
        if self.debug:
            human_input = input()
            if human_input != "c":
                return human_input
                        
        return action

    def _is_done(self, obs, action):
        # can implement a verification here that looks at the obs
        return action == "DONE"

    def act(self, objective):
        is_success = False
        while True:
            # get current observation (= browser content)
            obs = self.env.observation()
                
            # predict action
            action = self._get_llm_action(obs, objective)
            # low_level_action only one step
            if (self.skill_type == "low_level_action" and len(self.prev_actions) >=1):
                action = "DONE"
            # repeating actions
            if (len(self.prev_actions) >=1 and action == self.prev_actions[-1] and action!="scroll [down]" and action!="scroll [up]"):
                action = "DONE"
            
            # check if done
            if self._is_done(obs, action):
                is_success = True
                break

            # execute action
            self.env.step(action)
            
            self.prev_actions += [action]
            if len(self.prev_actions) >= self.max_iters:
                print(f'Reached limit of max iters in Low Level Policy: {len(self.prev_actions)}')
                break
            
            # If env is done, break
            if self.env.done():
                is_success = True
                break

        return is_success


class HighLevelTaskPolicy(Policy):
    def __init__(self, env, call_llm_fn, prompt_library, prompt="high_level_task", max_task_iters=5, max_policy_iters=5, task_debug=False, task_verbose=0, policy_debug=False, policy_verbose=0):
        self.env = env
        self.call_llm_fn = call_llm_fn   
        self.prompt_library = prompt_library

        self.base_prompt = getattr(self.prompt_library, prompt)
        self.prev_actions = []
        
        self.task_iters = 0
        self.max_task_iters = max_task_iters
        self.max_policy_iters = max_policy_iters
        self.task_debug = task_debug
        self.task_verbose = task_verbose
        self.policy_debug = policy_debug
        self.policy_verbose = policy_verbose
        

    def _get_llm_action(self, obs, objective):
        browser_content = obs

        prompt = add_latest_state_to_prompt(prompt=self.base_prompt, context=objective,
                                            url=self.env.url, browser_content=browser_content,
                                            prev_actions="\n".join(self.prev_actions))
        action, reason = self.call_llm_fn(prompt)
        
        
        if self.task_verbose > 0:
            if self.task_verbose > 1:
                print(browser_content)        
            print(f"\n Context: {objective}")
            prev_actions="\n".join(self.prev_actions)
            print(f"\n Previous Actions: {prev_actions}")
            print(f"\n Reason: {reason}")
            print(f"\n Action: {action}")
            
        if self.task_debug:
            human_input = input()
            if human_input != "c":
                return human_input

        return action

    def _parse_action_list(self, llm_action):
        action_list = llm_action.split("\n")
        return action_list

    def _is_done(self, obs, action):
        # can implement a verification here that looks at the obs
        return action == "DONE"

    def act(self):
        while not self.env.done():
            # Get objective
            objective = self.env.context()
            
            # get current observation (= browser content)
            obs = self.env.observation()

            # get list of actions on current webpage from LLM task planner
            llm_action = self._get_llm_action(obs, objective)
            action_list = self._parse_action_list(llm_action)
            
            # Note: Enforce last action in list to be done
            if action_list[-1] != "DONE":
                action_list.append("DONE")
            
            for action in action_list:
                if self._is_done(obs, action):
                    break

                action_type = action.split(" ")[0].lower()
                if action_type in VALID_SKILL_TYPES:  # call skill
                    skill_type = action_type
                elif action_type in VALID_ACTION_TYPES:
                    skill_type = "low_level_action"
                else:
                    skill_type = None
                
                if skill_type:
                    skill_policy = LowLevelSkillPolicy(env=self.env, call_llm_fn=self.call_llm_fn, 
                                                       prompt_library=self.prompt_library,
                                                       skill_type=skill_type, max_iters=self.max_policy_iters, debug=self.policy_debug, verbose=self.policy_verbose)
                    skill_policy.act(action)

                self.prev_actions += [action]
    
                if self.env.done():
                    break
            
            self.task_iters = self.task_iters + 1
            if (self.task_iters >= self.max_task_iters):
                print(f'Reached limit of max iters in High Level Task: {self.task_iters}')
                break;

        return False
