import openai
import os
import pandas as pd
import time

from miniwob.environment import MiniWoBEnvironment

from webactions_lm.policy.flat_policy import FlatPolicy
from webactions_lm.policy.heap_policy import HighLevelTaskPolicy
from webactions_lm.prompts.ablations import miniwob_flat_0, miniwob_flat_1, miniwob_flat_2, miniwob_heap_fewshot_0, miniwob_heap_fewshot_1, miniwob_heap_fewshot_2, miniwob_heap_fewshot_3, miniwob_heap_fewshot_4,miniwob_heap_fewshot_5, miniwob_heap_fewshot_6, miniwob_heap_fewshot_7
from webactions_lm.environment.miniwob import MiniWoBEnvironmentWrapper
from webactions_lm.utils.llm import call_llm

openai.api_key = os.environ.get('OPENAI_API_KEY')

df = None # pd.DataFrame(columns=['version', 'task', 'policy', 'seed', 'success', 'num_actions'])
data = {}

tasks = [
     "choose-date", 
      "copy-paste", # 
      "simple-algebra", 
      "find-word",
      "book-flight", 
      "search-engine",
]

seeds = range(10)
render_mode = None # "human", None
max_env_steps = 10
task_model_type = "text-davinci-003"  # gpt-4, text-davinci-003, gpt-3.5-turbo
policy_model_type =  "text-davinci-003"
policy_types = ["flat_fewshot", "heap_fewshot"]
call_llm_fn = lambda prompt: call_llm(prompt, model_type="text-davinci-003")
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/eval/miniwob/{timestr}.csv"

versions = range(8)

# Policies
def get_policy(policy_type, task_model_type, policy_model_type, version, env):
    if policy_type == "flat_fewshot":
        str = f"miniwob_flat_{version}"
        value = globals()[str]
        return FlatPolicy(env, model_type=policy_model_type, prompt_library=value, prompt="flat_fewshot", max_iters=25, verbose=0)
    elif policy_type == "heap_fewshot":
        str = f"miniwob_heap_fewshot_{version}"
        value = globals()[str]
        return HighLevelTaskPolicy(env, task_model_type=task_model_type, policy_model_type=policy_model_type, prompt_library=value, prompt="high_level_task", max_task_iters=4, task_debug=False, policy_debug=False, task_verbose=0, policy_verbose=0)

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    import tiktoken
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def print_token_lengths(versions, timestr):
    df_token_stats = None
    for version in versions:
        data['version'] = version
        for type in ["miniwob_flat", "miniwob_heap_fewshot"]:
            data['type'] = type
            if type == "miniwob_flat" and version > 3:
                continue
            file_name = f"{type}_{version}"
            file = globals()[file_name]
            for attr in dir(file):
                if not attr.startswith("__"):
                    prompt = getattr(file, attr)
                    if isinstance(prompt, str):
                        data['num_examples'] = prompt.count("EXAMPLE")
                        data['num_tokens'] = num_tokens_from_string(prompt, 'text-davinci-003')
                        df_token_stats = pd.concat([df_token_stats, pd.DataFrame([data])], ignore_index=True)
                        df_token_stats.to_csv(f"data/eval/ablations/token_stats_{timestr}.csv", index=False)

print_token_lengths(versions, timestr)

for version in versions:
    data['version'] = version
    for task in tasks:
        data['task'] = task
        for seed in seeds:
            data['seed'] = seed
            for policy_type in policy_types:
                data['policy'] = policy_type
                
                if policy_type == 'flat_fewshot' and version > 3:
                    continue
                
                max_retries = 5
                retry_delay = 2 # seconds
                for attempt in range(max_retries):
                    try:
                        miniwob_env = MiniWoBEnvironment(subdomain=task, wait_ms=600, render_mode=render_mode)
                        env = MiniWoBEnvironmentWrapper(miniwob_env=miniwob_env, seed=seed, max_steps=max_env_steps)
                        policy = get_policy(policy_type=policy_type, call_llm_fn=call_llm_fn, env=env)
                        policy.act()
                        miniwob_env.close()

                    except ConnectionResetError:
                        if attempt < max_retries - 1:
                            print(f"Connection was reset. Retrying in {retry_delay} seconds...")
                            time.sleep(retry_delay)
                            continue
                        else:
                            print("Max retries reached. Exiting.")
                            raise

                    break
            
                # Add success, task progress, excess actions to env()
                metrics = env.eval_metrics()
                for key, value in metrics.items():
                    data[key] = value
                    
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                print(df)
                df.to_csv(filename, index=False)