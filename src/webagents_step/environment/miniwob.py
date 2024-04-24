from webagents_step.parser import miniwob_parser
from webagents_step.environment.env import WebEnvironment

import re
from miniwob.action import create_element_click_action, create_focus_and_type_action
from miniwob.environment import MiniWoBEnvironment

import logging
logging.basicConfig(level=logging.ERROR)

class MiniWoBEnvironmentWrapper(WebEnvironment):
    def __init__(self, task, seed=None, max_browser_rows=125, 
                 max_steps=50, wait_ms=600, headless=False):
        
        render_mode = None if headless else "human"
        self.miniwob_env = MiniWoBEnvironment(subdomain=task, wait_ms=wait_ms, render_mode=render_mode)
        obs, _ = self.miniwob_env.reset(seed)

        self.obs = obs
        self.objective = obs["utterance"]
        self.url = ""
        self.max_browser_rows = max_browser_rows
        self.max_steps = max_steps
        self.steps = 0
        self.is_done = False
        self.reward = 0.0
        
    def reset(self, seed=None):
        obs, _ = self.miniwob_env.reset(seed)
        self.obs = obs

    def close(self):
        self.miniwob_env.close()
        
    def observation(self): # browser content
        dom_elements = self.obs['dom_elements']
        browser_content = miniwob_parser.parse_dom_browser_content(
            dom_elements, process_dates=True)
        browser_content = browser_content[:self.max_browser_rows]
        browser_content = "\n".join(browser_content)
        return browser_content
    
    def get_url(self):
        return self.url
    
    def done(self):
        if self.is_done:
            return True
        return False

    def parse_action(self, action):
        """
        Parse a given action based on the action type,
        - click [id]: Clicks an element based on the provided id.
        - type [id] [content]: Types the provided content into the element with the specified id.
        - stop [response]: Stops execution and optionally provides a response.
        """
        if not action:
            print("Action text is None")
            return None

        click_match = re.match(r"click \[(\S+)\]", action, re.IGNORECASE)
        type_match = re.match(r"type \[(\S+)\] \[(.+)\]", action, re.IGNORECASE)
        stop_match = re.match(r"stop \[([^\]]*)\]", action, re.IGNORECASE)

        action_cmd = None
        if click_match:
            id = click_match.group(1)
            action_cmd = create_element_click_action(int(id)) if id.isdigit() else None
        elif type_match:
            id = type_match.group(1)
            content = type_match.group(2)
            action_cmd = create_focus_and_type_action(int(id), content) if id.isdigit() else None
        elif stop_match:
            self.response = stop_match.group(1)
            self.is_done = True
            action_cmd = None
        else:
            print(f"[MiniWoBEnvironmentWrapper::parse_action] Error {action} not defined")
        
        return action_cmd
    
    def status(self):
        return {'done': self.is_done, 'reward': self.reward, 'success': float(self.reward > 0), 'num_actions': self.steps}

    def step(self, action):
        self.steps = self.steps + 1
        print(f"[Step {self.steps}] {action}")
        
        if self.steps > self.max_steps:
            print(f"Steps {self.steps} exceeded maximum {self.max_steps}")
            self.is_done = True
            self.reward = -1
            return self.status()

        action_cmd = self.parse_action(action)
        if action_cmd:
            try:
                obs, reward, done, truncated, info = self.miniwob_env.step(action_cmd)
                self.obs = obs
                if "raw_reward" in info:
                    self.reward = info['raw_reward']
                else:
                    self.reward = reward
                self.is_done = done
            except Exception as e:
                print(f"Error occurred while taking step: {e}")
            
        return self.status()
    
    def get_objective(self):
        return self.objective 