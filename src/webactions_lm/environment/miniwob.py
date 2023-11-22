from webactions_lm.environment.env import WebEnvironment
from webactions_lm.parser import miniwob_parsers

class MiniWoBEnvironmentWrapper(WebEnvironment):
    def __init__(self, miniwob_env, seed=None, max_browser_rows=125, max_steps=50):
        self.miniwob_env = miniwob_env
        obs, info = self.miniwob_env.reset(seed)
        self.obs = obs
        self.url = ""
        self.max_browser_rows = max_browser_rows
        self.raw_metrics = {}
        self.max_steps = max_steps
        self.steps = 0
        
    def reset(self, seed=None):
        obs, info = self.miniwob_env.reset(seed)
        self.obs = obs
        
    def observation(self): # browser content
        dom_elements = self.obs['dom_elements']
        browser_content = miniwob_parsers.parse_dom_browser_content(
            dom_elements, ignore_tags=[], process_dates=True)
        browser_content = browser_content[:self.max_browser_rows]
        browser_content = "\n".join(browser_content)
        return browser_content

    def context(self):
        return self.obs["utterance"]
    
    def done(self):
        if self.raw_metrics:
            return self.raw_metrics['done']
        else:
            return False
    
    def eval_metrics(self):
        if self.raw_metrics and self.raw_metrics['done'] == True:
            metrics = {'success': float(self.raw_metrics['reward'] > -1), 'task_progress': float(self.raw_metrics['reward'] > -1), 'num_actions': self.steps}
        else:
             metrics = {'success': False, 'task_progress': 0.0, 'num_actions': self.steps}
        return metrics

    def step(self, action):
        self.steps = self.steps + 1
        print(f"Step {self.steps} action {action}")
        if self.steps <= self.max_steps:
            action_cmd = miniwob_parsers.parse_action(action)
            if action_cmd:
                try:
                    obs, reward, done, truncated, info = self.miniwob_env.step(action_cmd)
                    self.obs = obs
                    if "raw_reward" in info:
                        self.raw_metrics['reward'] = info['raw_reward']
                    else:
                        self.raw_metrics['reward'] = reward
                    self.raw_metrics['done'] = done
                    self.raw_metrics['info'] = info
                except Exception as e:
                    print(f"Error occurred while taking step: {e}")
            else:
                print(f"Could not parse action {action}. Skipping.")
        else:
            print(f"Number of steps {self.steps} exceeded maximum {self.max_steps}")
            self.raw_metrics['done'] = True
            self.raw_metrics['reward'] = -1
        