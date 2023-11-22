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
from webactions_lm.utils.llama_util import load_model, load_tokenizer, call_llm_llama

openai.api_key = os.environ.get('OPENAI_API_KEY')

df = None # pd.DataFrame(columns=['task', 'seed', 'policy', 'success', 'task_progress', 'excess_actions'])
data = {}

single_tasks = ['click-link', 'click-option', 'focus-text', 'click-button', 'click-button-sequence', 'click-dialog', 'click-dialog-2', 'click-tab', 'click-test', 'click-test-2', 'enter-text', 'focus-text-2', 'enter-text-dynamic', 'enter-password', 'login-user', 'click-pie', 'enter-date', 'grid-coordinate', 'click-widget']

complex_tasks = [ 'email-inbox', 'email-inbox-nl-turk', 'email-inbox-forward-nl-turk', 'multi-orderings', 'choose-date', 'click-collapsible-2', 'simple-arithmetic', 'click-tab-2', 'click-tab-2-hard', 'multi-layouts', 'copy-paste', 'click-collapsible', 'choose-date-easy', 'copy-paste-2', 'simple-algebra', 'click-checkboxes', 'click-checkboxes-transfer', 'login-user-popup', 'click-checkboxes-soft', 'enter-text-2', 'email-inbox-forward-nl', 'search-engine', 'find-word', 'choose-date-medium', 'click-checkboxes-large', 'book-flight']


tasks = single_tasks + complex_tasks 
seeds = range(50)
render_mode = None # "human" # None
max_env_steps = 15 
policy_types = ["flat_zeroshot", "heap_zeroshot", "flat_fewshot", "heap_fewshot"]
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/eval/miniwob/{timestr}.csv"

call_llm_fn = lambda prompt: call_llm(prompt, model_type="text-davinci-003teh")

# Use LLAMA model
# model_path = "anonymous/Llama-2-13b-chat-hf"
# tokenizer = load_tokenizer(model_path, context_size=4096)
# model = load_model(model_path, dtype="bf16", context_len=4096)
# model.eval()
# call_llm_fn = lambda prompt: call_llm_llama(prompt, model, tokenizer)

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

for task in tasks:
    data['task'] = task
    for seed in seeds:
        data['seed'] = seed
        for policy_type in policy_types:
            data['policy'] = policy_type
            
            max_retries = 5
            retry_delay = 2 
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