from webagents_step.agents.agent import Agent
from typing import List

class PlaybackAgent(Agent):
    def __init__(self, max_actions: int = 1e6, verbose: bool = False, logging: bool = False, 
                 debug: bool = False, playback_trajectory=None, previous_actions: List = None):
        super().__init__(max_actions=max_actions, verbose=verbose, logging=logging, previous_actions=previous_actions)
        self.debug = debug
        # List of dictionary with atleast the action, reason key
        self.playback_trajectory = playback_trajectory
        self.max_actions = len(self.playback_trajectory)

    def predict_action(self, objective, observation, url=None):
        index = len(self.previous_actions)
         
        if index < len(self.playback_trajectory):
            action = self.playback_trajectory[index]['action']
            reason = self.playback_trajectory[index]['reason']
            
            if self.verbose > 0:
                if self.verbose > 1:
                    print(f"\n OBSERVATION: {observation}")      
                print(f"\n OBJECTIVE: {objective}")
                print(f'\n PREVIOUS ACTIONS: {self.previous_actions}')
                print(f"\n REASON: {reason}")
                print(f"\n ACTION: {action}")
                
            if self.debug:
                human_input = input()
                if human_input != "c":
                    action = human_input
                    reason = "None" 
            
            self.update_history(action=action, reason=reason)
            return action, reason
        return None, None