from webagents_step.agents.agent import Agent
from webagents_step.utils.llm import fill_prompt_template, construct_llm_message_hf, generate_prediction, parse_action_reason
from typing import Dict


class FineTunedAgent(Agent):
    def __init__(self, max_actions=10, verbose=0, logging=False, debug=False, model=None, tokenizer=None, prompt_template=None, prompt_mode="completion", model_type="llama2", model_kwargs: Dict = None):
        super().__init__(max_actions=max_actions, verbose=verbose, logging=logging)
        self.debug = debug
        self.model = model
        self.tokenizer = tokenizer
        self.prompt_template = prompt_template
        self.prompt_mode = prompt_mode
        self.model_type = model_type
        self.model_kwargs = model_kwargs
        
        self.model.eval()
        
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
            previous_history="\n".join(self.previous_actions)
            
        return previous_history

    def predict_action(self, objective, observation, url=None):   
        prompt = fill_prompt_template(prompt_template=self.prompt_template, objective=objective, 
                                      observation=observation, url=url, 
                                      previous_history=self.previous_history())
        messages = construct_llm_message_hf(prompt=prompt, prompt_mode=self.prompt_mode, model_type=self.model_type)

        inputs = messages[0]["content"] # todo: generalize to 'chat' mode
        model_response = generate_prediction(inputs=inputs, model=self.model, tokenizer=self.tokenizer, **self.model_kwargs)        
        action, reason = parse_action_reason(model_response)
        
        if self.logging:
            self.data_to_log['input'] = inputs
            self.data_to_log['model_response'] = model_response

        if self.verbose > 0:
            if self.verbose > 1:
                print(f"\n OBSERVATION: {observation}")
                print(f"\n RESPONSE: {model_response}")        
            print(f"\n OBJECTIVE: {objective}")
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