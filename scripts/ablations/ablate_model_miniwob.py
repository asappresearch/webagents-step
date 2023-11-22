import openai
import os
import pandas as pd
import time

from miniwob.environment import MiniWoBEnvironment

from webactions_lm.policy.flat_policy import FlatPolicy
from webactions_lm.policy.heap_policy import HighLevelTaskPolicy
from webactions_lm.prompts.miniwob import miniwob_flat, miniwob_heap_zeroshot, miniwob_heap_fewshot
from webactions_lm.environment.miniwob import MiniWoBEnvironmentWrapper
from webactions_lm.utils.llm import call_llm

openai.api_key = os.environ.get('OPENAI_API_KEY')

df = None # pd.DataFrame(columns=['task', 'seed', 'policy', 'success', 'task_progress', 'excess_actions'])
data = {}

tasks = [
    "book-flight",
    "search-engine",
    "simple-algebra",
]

seeds = range(50)
render_mode = None # "human" # None
max_env_steps = 15 # No env should need more than 15 steps to succeed
model_types = ["gpt-4", "gpt-3.5-turbo", "text-davinci-003"]
policy_types = ["flat_zeroshot", "heap_zeroshot", "flat_fewshot", "heap_fewshot"]
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/eval/miniwob/{timestr}.csv"

# Policies
def get_policy(policy_type, call_llm_fn, env):
    if policy_type == "flat_zeroshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=miniwob_flat, prompt="flat_zeroshot", max_iters=25, verbose=2, debug=False)   
    elif policy_type == "flat_fewshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=miniwob_flat, prompt="flat_fewshot", max_iters=25, verbose=2, debug=False)
    elif policy_type == "heap_zeroshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=miniwob_heap_zeroshot, prompt="high_level_task",  max_task_iters=4, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)
    elif policy_type == "heap_fewshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=miniwob_heap_fewshot, prompt="high_level_task", max_task_iters=10, max_policy_iters=10, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)

counter_to_start = 6
counter = -1
for model_type in model_types:
    data['model'] = model_type
    call_llm_fn = lambda prompt: call_llm(prompt, model_type=model_type)
    for task in tasks:
        if (task == "book-flight"): continue
        data['task'] = task
        for seed in seeds:
            data['seed'] = seed
            for policy_type in policy_types:
                data['policy'] = policy_type
                
                counter = counter + 1
                print(f"Counter: {counter} Model:{model_type} Seed: {seed} Policy:{policy_type}")
                if counter < counter_to_start:
                    continue
                data['counter'] = counter
                
                miniwob_env = MiniWoBEnvironment(subdomain=task, wait_ms=600, render_mode=render_mode)
                env = MiniWoBEnvironmentWrapper(miniwob_env=miniwob_env, seed=seed, max_steps=max_env_steps)
                policy = get_policy(policy_type=policy_type, call_llm_fn=call_llm_fn, env=env)
                            
                # Act
                policy.act()
                miniwob_env.close()
                
                # Add success, task progress, excess actions to env()
                metrics = env.eval_metrics()
                for key, value in metrics.items():
                    data[key] = value
                    
                df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
                print(df)
                df.to_csv(filename, index=False)
