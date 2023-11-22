import re
import pandas as pd
from time import sleep

from webactions_lm.environment.env import WebEnvironment
from webactions_lm.parser import liveweb_parsers

class LiveWebEnvironmentWrapper(WebEnvironment):
    def __init__(self, context, url, max_browser_rows=150, max_steps=50):
        self.context_val = context
        self.url = url
        self.max_browser_rows = max_browser_rows

        # self.parser = heihei_parser.WebUIHeiHei() # use browser plugin
        self.parser = liveweb_parsers.LiveWebParser() # use playwright
        self.parser.go_to_page(self.url)

        self.timestep = 0
        self._log = pd.DataFrame(columns=['time_step', 'browser_content', 'action'])
        self.max_steps = max_steps
        self.steps = 0
        self.is_done = False
        self.clear_presets()
            
    def clear_presets(self):
        self.parser.parse_page()
        if "aa.com" in self.url:
            self.parser.clear(42)
        if "united.com" in self.url:
            self.parser.clear(43)
            self.parser.clear(51)
            self.parser.clear(53)
            self.parser.clear(51)
            self.parser.clear(53)
            self.parser.clear(51)
            self.parser.clear(53)
            self.parser.click(43)
        if "jetblue.com" in self.url:
            self.parser.page.mouse.click(829, 307)
            # self.parser.page.mouse.click(929, 257)

    def reset(self):
        self.close()
        self.__init__(self.context_val, self.url)
        self.clear_presets()
    
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
                    # text = re.search(r"'(.+?)'").strip('"')
                    text = action.split(" ")[-1].strip('"')
                    # text += '\n'
                    self.parser.type(id, text)
                elif action.startswith("CLEAR"):
                    id = action.split(" ")[1]
                    if isinstance(id, int): raise Exception("Id not a valid integer")
                    self.parser.clear(id)
                else:
                    print(f"Error occurred while taking step: {action} not defined")
                sleep(delay)
            except Exception as e:
                print(f"Error occurred while parsing action: {action}")
        else:
            print(f"Number of steps {self.steps} exceeded maximum {self.max_steps}")
            self.is_done = True
        
    def done(self):
        if "united.com" in self.url:
            if self.parser.page.url != 'https://www.united.com/en/us':
                return True
        if "aa.com" in self.url:
            if self.steps >=6:
                return True
        return self.is_done
    
    def eval_metrics(self):
        pass