from webactions_lm.policy.policy import Policy
from webactions_lm.utils.llm import add_latest_state_to_prompt

class FlatPolicy(Policy):
    def __init__(self, env, call_llm_fn, prompt_library, prompt, max_iters=50, debug=False, verbose=0):
        self.env = env
        self.call_llm_fn = call_llm_fn
        self.prompt_library = prompt_library
        self.base_prompt = getattr(self.prompt_library, prompt)
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
        
        if self.debug:
            human_input = input()
            if human_input != "c":
                return human_input
                        
        return action

    def _is_done(self, obs, action):
        return action == "DONE"

    def act(self):
        while not self.env.done():
            # Get objective
            objective = self.env.context()
            
            # get current observation / browser content
            obs = self.env.observation()
                
            # predict action
            action = self._get_llm_action(obs, objective)
            
            # check if done
            if self._is_done(obs, action):
                break
            
            # execute action
            self.env.step(action)
            
            self.prev_actions += [action]
            
            if len(self.prev_actions) >= self.max_iters:
                print(f'Reached limit of max iters in Flat Policy: {len(self.prev_actions)}')
                break

        return True
