from webagents_step.agents.agent import Agent

class KeyboardAgent(Agent):
    def __init__(self, max_actions: int = 10, verbose: bool = False, logging: bool = False):
        super().__init__(max_actions=max_actions, verbose=verbose, logging=logging)
    
    def predict_action(self, objective, observation, url=None):
        print(f"\n OBJECTIVE: {objective}")
        print(f"\n OBSERVATION: {observation}")
        print(f'\n PREVIOUS ACTIONS: {self.previous_actions}')        
        action = input()

        self.update_history(action=action, reason="")
        return action, None