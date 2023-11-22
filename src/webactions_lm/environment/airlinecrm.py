
import re
import json
import pandas as pd
from time import sleep

from webactions_lm.utils.web import read_webpage_content
from webactions_lm.environment.env import WebEnvironment
from webactions_lm.parser import liveweb_parsers

class AirlineCRMEnvironmentWrapper(WebEnvironment):
    def __init__(self, context, scenario, max_browser_rows=150, max_steps=50):
        self.context_val = context
        self.scenario = scenario
        self.max_browser_rows = max_browser_rows
        self.timestep = 0
        self._log = pd.DataFrame(columns=['time_step', 'browser_content', 'action'])
        self.raw_metrics = {}
        self.max_steps = max_steps
        self.steps = 0
        self.is_done = False
        
        self.reset_scenario()
        self.url = f"https://airlinecrm.awsdev.anonymous.com/?scenario={self.scenario}"
        self.parser = liveweb_parsers.LiveWebParser()
        self.parser.go_to_page(self.url)
        sleep(1.0)

    def reset(self):
        self.close()
        self.__init__(self.context_val, self.url)
        
    def reset_scenario(self):
        reset_url = f"https://airlinecrm.awsdev.anonymous.com/reset-scenario?scenario={self.scenario}"
        read_webpage_content(reset_url)
    
    def close(self):
        self.parser.close()

    def observation(self):
        browser_content = self.parser.parse_page()
        browser_content = browser_content[:self.max_browser_rows]
        browser_content = "\n".join(browser_content)
        return browser_content

    def context(self):
        return self.context_val
    
    def log(self):
        return self._log

    def step(self, action, delay=1.0):
        self.steps = self.steps + 1
        print(f"Step {self.steps} action {action}")
        if self.steps <= self.max_steps:
            # Update log
            datapoint = {'time_step': [self.timestep], 'browser_content': [self.observation()], 'action': [action]}
            self._log = pd.concat([self._log, pd.DataFrame(datapoint)], ignore_index=True)

            try:
                if action.startswith("CLICK"):
                    id = action.split(" ")[1]
                    if isinstance(id, int): raise Exception("Id not a valid integer")
                    self.parser.click(id)
                elif action.startswith("TYPE"):
                    id = action.split(" ")[1]
                    if isinstance(id, int): raise Exception("Id not a valid integer")
                    match = re.search(r'\b\d+\s+(.*)$', action)
                    text = match.group(1)
                    text = text.strip('"')
                    self.parser.type(id, text)
                elif action.startswith("CLEAR"):
                    id = action.split(" ")[1]
                    if isinstance(id, int): raise Exception("Id not a valid integer")
                    self.parser.clear(id)
                else:
                    print(f"Error occurred while taking step: {action} not defined")
            except Exception as e:
                print(f"Error occurred while parsing action: {action}")
            
            sleep(delay)
            self.update_raw_metrics()
            if self.raw_metrics and self.raw_metrics['success'] >=1.:
                self.is_done = True
        else:
            print(f"Number of steps {self.steps} exceeded maximum {self.max_steps}")
            self.is_done = True       
    
    def update_raw_metrics(self):
        evaluation_url = f"https://airlinecrm.awsdev.anonymous.com/evaluate?scenario={self.scenario}"
        raw_evaluation = json.loads(read_webpage_content(evaluation_url))
        metrics = raw_evaluation['metrics'][-1] #Get the last metrics
        self.raw_metrics['success'] = float(metrics['task_completion'])
        self.raw_metrics['task_progress'] = float(metrics["%complete"])

    def done(self):
        return self.is_done 
    
    def eval_metrics(self):
        if self.raw_metrics:
            metrics = {'success': self.raw_metrics['success'], 'task_progress': self.raw_metrics['task_progress'], 'num_actions': self.steps}
        else:
            metrics = {'success': 0.0, 'task_progress': 0.0, 'num_actions': self.steps}
        return metrics