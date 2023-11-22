import os
os.environ[
    "SHOPPING"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:7770"
os.environ[
    "SHOPPING_ADMIN"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:7780/admin"
os.environ[
    "REDDIT"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:9999"
os.environ[
    "GITLAB"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:8023"
os.environ[
    "MAP"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:3000"
os.environ[
    "WIKIPEDIA"
] = "http://ec2-3-131-244-37.us-east-2.compute.amazonaws.com:8888/wikipedia_en_all_maxi_2022-05/A/User:The_other_Kiwix_guy/Landing"
os.environ[
    "HOMEPAGE"
] = "PASS"  # The home page is not currently hosted in the demo site

import json
from webactions_lm.environment.env import WebEnvironment

# Init an environment
from browser_env import (
    create_id_based_action,
    StateInfo,
    Trajectory,
    ActionTypes
)
from evaluation_harness.evaluators import evaluator_router


class WebArenaEnvironmentWrapper(WebEnvironment):
    def __init__(self, webarena_env, config_file, max_steps=50, max_browser_content=6000):
        self.webarena_env = webarena_env
        self.config_file = config_file
        with open(self.config_file, "r") as f:
            self.config = json.load(f)

        self.obs, self.info = self.webarena_env.reset(options={"config_file": self.config_file})
        self.terminated = False
        self.raw_metrics = {'success': False, 'task_progress': 0.0, 'num_actions': 0, 'info': None}
        self.max_steps = max_steps
        self.steps = 0
        self.max_browser_content = max_browser_content
        self.stop_action = False
        
        self.url = self.config["start_url"]
        
        self.trajectory: Trajectory = []
        self.update_trajectory()
        
    def reset(self, seed=None):
        self.obs, self.info = self.webarena_env.reset(options={"config_file": self.config_file})
        
    def close(self):
        self.webarena_env.close()
        
    def observation(self): # browser content
        self.obs = self.webarena_env._get_obs()
        browser_content = self.obs["text"]
        
        browser_content = browser_content[:self.max_browser_content]
        # print (len(browser_content))
        return browser_content

    def context(self):
        return self.config["intent"]
    
    def done(self):
        return (self.raw_metrics['success'] >= 1.0) or self.terminated or (self.steps >= self.max_steps) or self.stop_action
    
    def eval_metrics(self):
        metrics = {k: self.raw_metrics[k] for k in ['success', 'task_progress', 'num_actions']}
        return metrics

    def step(self, action):
        self.steps = self.steps + 1
        print(f"Step {self.steps} action {action}")
        if self.steps <= self.max_steps:
            try:
                action_cmd = create_id_based_action(action)
                self.obs, _, self.terminated, _, self.info = self.webarena_env.step(action_cmd)
                self.update_trajectory(action_cmd)
                self.update_raw_metrics()
            except Exception as e:
                print(f"Error occurred while taking action: {e}")
        else:
            print(f"Number of steps {self.steps} exceeded maximum {self.max_steps}")
            
    def update_trajectory(self, action_cmd=None):
        # Append action (if any) and resulting sate
        if action_cmd:
            self.trajectory.append(action_cmd)
            if action_cmd["action_type"]== ActionTypes.STOP:
                # We are done, no need to append state
                self.stop_action = True
                return 
        # Append the resulting state info 
        state_info: StateInfo = {"observation": self.obs, "info": self.info}
        self.trajectory.append(state_info)
            
    def update_raw_metrics(self):
        try:
            evaluator = evaluator_router(self.config_file)
            score = evaluator(trajectory=self.trajectory, config_file=self.config_file, page=self.webarena_env.page, client=self.webarena_env.get_page_client(self.webarena_env.page))
        except Exception as e:
            score = 0
        self.raw_metrics['success'] = score
        self.raw_metrics['task_progress'] = self.raw_metrics['success']
        self.raw_metrics['num_actions'] = self.steps
