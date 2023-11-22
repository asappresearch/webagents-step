import openai
import os
import pandas as pd
import time
import json

from webactions_lm.environment.webarena import WebArenaEnvironmentWrapper

from webactions_lm.policy.flat_policy import FlatPolicy
from webactions_lm.policy.heap_policy import HighLevelTaskPolicy
from webactions_lm.prompts.webarena import webarena_flat, webarena_heap_zeroshot, webarena_heap_fewshot
from webactions_lm.utils.llm import call_llm

openai.api_key = os.environ.get('OPENAI_API_KEY')

# Init an environment
from browser_env import ScriptBrowserEnv

config_file_list = []

ids = [132]

for id in ids:
    config_file_list.append(f"data/webarena_config_files/{id}.json")
    
# Policies
def get_policy(policy_type, call_llm_fn, env):
    if policy_type == "flat_zeroshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=webarena_flat, prompt="flat_zeroshot", max_iters=25, verbose=2, debug=False)   
    elif policy_type == "flat_fewshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=webarena_flat, prompt="flat_fewshot", max_iters=25, verbose=2, debug=False)
    elif policy_type == "heap_zeroshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=webarena_heap_zeroshot, prompt="high_level_task",  max_task_iters=4, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)
    elif policy_type == "heap_fewshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=webarena_heap_fewshot, prompt="high_level_task", max_task_iters=10, max_policy_iters=10, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)

# Seeds
policy_types = ["flat_zeroshot", "heap_zeroshot", "flat_fewshot", "heap_fewshot"]
call_llm_fn = lambda prompt: call_llm(prompt, model_type="text-davinci-003")
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/eval/webarena/{timestr}.csv"
max_env_steps = 10 # No env should need more than 15 steps to succeed
max_browser_content = 6000

df = None 
data = {}
for config_file in config_file_list:
    data['config_file'] = config_file
    with open(config_file, "r") as f:
        config = json.load(f)
    data['site'] = config['sites'][0]
    print(config['intent'])
    for policy_type in policy_types:
        data['policy'] = policy_type
        try:
            for attempt in (0,2):
                # Init the environment
                webarena_env = ScriptBrowserEnv(
                    headless=False,
                    slow_mo=1,
                    observation_type="accessibility_tree",
                    current_viewport_only=True,
                    viewport_size={"width": 1280, "height": 720},
                )
                env = WebArenaEnvironmentWrapper(webarena_env, config_file, max_steps=max_env_steps, max_browser_content=max_browser_content)
                policy = get_policy(policy_type=policy_type, call_llm_fn=call_llm_fn, env=env)
                
                # Act
                policy.act()
                env.close()
                
                break
                
            # Add success, task progress, excess actions to env()
            metrics = env.eval_metrics()
            for key, value in metrics.items():
                data[key] = value
            
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            print(df)
            df.to_csv(filename, index=False)
        except Exception as e:
            print(f"Exception occurred: {e}")
        

