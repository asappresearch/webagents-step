from webagents_step.agents.agent import Agent
from typing import List
from webagents_step.utils.llm import fill_prompt_template, construct_llm_message_openai, call_openai_llm, parse_action_reason, calculate_cost_openai

class PromptAgent(Agent):
    def __init__(self, max_actions: int = 10, verbose: bool = False, logging: bool = False, 
                 debug: bool = False, prompt_template: str = None, model: str = "gpt-3.5-turbo", 
                 prompt_mode: str = "chat", previous_actions: List = None, previous_reasons: List = None, previous_responses: List = None):
        super().__init__(max_actions=max_actions, verbose=verbose, logging=logging, previous_actions=previous_actions, previous_reasons=previous_reasons, previous_responses=previous_responses)        
        self.debug = debug 
        self.prompt_template = prompt_template
        self.model = model
        self.prompt_mode = prompt_mode

    def previous_history(self):
        previous_history = []
        
        if len(self.previous_actions) == len(self.previous_responses):
            for action, response in zip(self.previous_actions, self.previous_responses):
                if response:
                    previous_history.append(f"{response} = {action}")
                else:
                    previous_history.append(action)
            previous_history="\n".join(previous_history)
        else:
            previous_history = "\n".join(action for action in self.previous_actions if action is not None) if self.previous_actions is not None else ""

            
        return previous_history

    def predict_action(self, objective, observation, url=None):
        prompt = fill_prompt_template(prompt_template=self.prompt_template, objective=objective, 
                                      observation=observation, url=url, 
                                      previous_history=self.previous_history())
        messages = construct_llm_message_openai(prompt=prompt, prompt_mode=self.prompt_mode)
        model_response = call_openai_llm(messages=messages, model=self.model)
        action, reason = parse_action_reason(model_response)
                
        if self.logging:
            self.data_to_log['prompt'] = messages
        
        if self.verbose > 0:
            if self.verbose > 1:
                print(f"\n OBSERVATION: {observation}")
                print(f"\n RESPONSE: {model_response}")        
            print(f"\n OBJECTIVE: {objective}")
            print(f"\n URL: {url}")
            print(f"\n PREVIOUS HISTORY: {self.previous_history()}")
            print(f"\n REASON: {reason}")
            print(f"\n ACTION: {action}")
        
        if self.debug:
            human_input = input()
            if human_input != "c":
                action = human_input
                reason = "None"

        self.update_history(action=action, reason=reason)
        return action, reason