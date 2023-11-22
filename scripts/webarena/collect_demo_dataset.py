import os
import pandas as pd
import json
from termcolor import colored

from webactions_lm.environment.webarena import WebArenaEnvironmentWrapper

# Init an environment
from browser_env import ScriptBrowserEnv

# Init the environment
webarena_env = ScriptBrowserEnv(
    headless=False,
    slow_mo=100,
    observation_type="accessibility_tree",
    current_viewport_only=True,
    viewport_size={"width": 1280, "height": 720},
)

# Load a config
config_file = "data/webarena_config_files/119.json"
with open(config_file) as f:
    config = json.load(f)

save_dir = "data/demos/webarena"
output_file = f"{save_dir}/flight_demos_across_uis.csv"
if os.path.isfile(output_file):
    df = pd.read_csv(output_file)
else:
    df = pd.DataFrame(
        columns=['context', 'url', 'episode', 'time_step', 'browser_content', 'action'])

env = WebArenaEnvironmentWrapper(webarena_env, config_file)

actions = "click [id], type [id] [content] [press_enter_after=0|1], hover [id], press [key_comb], scroll [direction=down|up], new_tab, tab_focus [tab_index], close_tab, goto [url], go_back, go_forward, stop [answer]"

time_step = 0
while not env.done():
    browser_content = env.observation()
    print("==" * 60)
    print(colored(env.context(), "red"))
    print("==" * 60)
    print(colored(browser_content, "cyan"))
    print("==" * 60)
    print(f'Your action? Choose between {actions}')
    action = input()
    env.step(action)
    
    metrics = env.eval_metrics()
    print(metrics)
    time_step = time_step + 1

env.close()

print(f"Saving demo data to {output_file}")
df.to_csv(output_file, index=False)

