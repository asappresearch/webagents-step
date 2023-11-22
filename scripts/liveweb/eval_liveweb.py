import openai
import os
import time
import pandas as pd
from webactions_lm.policy.flat_policy import FlatPolicy
from webactions_lm.policy.heap_policy import HighLevelTaskPolicy
from webactions_lm.environment.liveweb import LiveWebEnvironmentWrapper
from webactions_lm.prompts.liveweb import liveweb_flat, liveweb_heap_zeroshot, liveweb_heap_fewshot
from webactions_lm.utils.llm import call_llm

openai.api_key = os.environ.get('OPENAI_API_KEY')
 
df = pd.DataFrame()
data = {}

# Policies
def get_policy(policy_type, call_llm_fn, env):
    if policy_type == "flat_zeroshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=liveweb_flat, prompt="flat_zeroshot", max_iters=25, verbose=2, debug=False)   
    elif policy_type == "flat_fewshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=liveweb_flat, prompt="flat_fewshot", max_iters=25, verbose=2, debug=False)
    elif policy_type == "heap_zeroshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=liveweb_heap_zeroshot, prompt="high_level_task",  max_task_iters=4, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)
    elif policy_type == "heap_fewshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=liveweb_heap_fewshot, prompt="high_level_task", max_task_iters=10, max_policy_iters=10, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)


# Seeds
call_llm_fn = lambda prompt: call_llm(prompt, model_type="text-davinci-003")
policy_types = ["flat_zeroshot", "heap_zeroshot", "flat_fewshot", "heap_fewshot"]
env_max_steps = 10
timestr = time.strftime("%Y%m%d-%H%M%S")
eval_filename = f"data/eval/liveweb/{timestr}.csv"

# Load a set of demonstrations
# Assume that one CSV corresponds to a set of episodes, and we will compute rollouts for each episode
#columns=['episode', 'time_step', 'context', 'url', 'browser_content', 'action'])
df_demo = pd.read_csv(f'data/demos/liveweb/flight_demos_across_uis_augmented.csv')

# group the DataFrame by 'episode'
groups = df_demo.groupby('episode')


# Create a dataframe to log rollouts
#columns=['policy', 'episode', 'time_step', 'context', 'url', 'browser_content', 'action'])

episode_to_resume_from = 0
df_log_list = []
for episode, df_episode in groups:
    if episode < episode_to_resume_from:
        continue
    print(f"Episode {episode} Url {df_episode.iloc[0]['url']}:")
    for policy_type in policy_types:
        context = df_episode.iloc[0]['context']
        url = df_episode.iloc[0]['url']

        env = LiveWebEnvironmentWrapper(context=context, url=url, max_browser_rows=100, max_steps=8)
        policy = get_policy(policy_type=policy_type, call_llm_fn=call_llm_fn, env=env)

        policy.act()
        env.close()
        
        df_log = env.log()

        df_log['episode'] = episode
        df_log['context'] = context
        df_log['url'] = url
        df_log['policy'] = policy_type
        df_log_list.append(df_log)
        df_logs = pd.concat(df_log_list, axis=0, ignore_index=True)
        df_logs.to_csv(eval_filename, index=False)
