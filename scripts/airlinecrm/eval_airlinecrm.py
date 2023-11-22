import openai
import os
import pandas as pd
import time
import json

from webactions_lm.environment.miniwob import AirlineCRMEnvironmentWrapper
from webactions_lm.utils.web import read_webpage_content
from webactions_lm.utils.generate_context_airlinecrm import generate_context_airlinecrm

from webactions_lm.policy.flat_policy import FlatPolicy
from webactions_lm.policy.heap_policy import HighLevelTaskPolicy
from webactions_lm.prompts.airlinecrm import ailrinecrm_heap_zeroshot, airlinecrm_heap_fewshot, airline_flat
from webactions_lm.utils.llm import call_llm

openai.api_key = os.environ.get('OPENAI_API_KEY')

df = pd.DataFrame()
data = {}

tasks = [
	'TASK_CANCEL_FLIGHT',
    'TASK_FIND_BOOKING',
    'TASK_FIND_FLIGHT',
    'TASK_UPDATE_PASSENGER_DETAILS',
    'TASK_BOOK_FLIGHT',
]

env_max_steps = {'TASK_UPDATE_PASSENGER_DETAILS': 15, 'TASK_BOOK_FLIGHT': 25}

# Create a set of problems by calling https://airlinecrm.awsdev.anonymous.com/get-random-scenario?task=TASK_CANCEL_FLIGHT
# Df of task, scenario, context
df_problems = None
load_problem_from_file = True
problem_filename = f"data/demos/airlinecrm/problems_updatepassenger_bookflight.csv"
if not load_problem_from_file:
    num_scenarios = 15
    for task in tasks:
        get_scenario_url = f"https://airlinecrm.awsdev.anonymous.com/get-random-scenario?task={task}"
        for i in range(num_scenarios):
            scenario_info = json.loads(read_webpage_content(get_scenario_url))
            data = {}
            data['task'] = task
            data['scenario'] = scenario_info['id']
            data['context'] = generate_context_airlinecrm(task, scenario_info['details'])
            df_problems = pd.concat([df_problems, pd.DataFrame([data])], ignore_index=True)
    df_problems.to_csv(problem_filename, index=False)
else:
    df_problems = pd.read_csv(problem_filename)
    
# Policies
def get_policy(policy_type, call_llm_fn, env):
    if policy_type == "flat_zeroshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=airline_flat, prompt="flat_zeroshot", max_iters=25, verbose=2, debug=False)   
    elif policy_type == "flat_fewshot":
        return FlatPolicy(env, call_llm_fn=call_llm_fn, prompt_library=airline_flat, prompt="flat_fewshot", max_iters=25, verbose=2, debug=False)
    elif policy_type == "heap_zeroshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=ailrinecrm_heap_zeroshot, prompt="high_level_task",  max_task_iters=4, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)
    elif policy_type == "heap_fewshot":
        return HighLevelTaskPolicy(env, call_llm_fn=call_llm_fn, prompt_library=airlinecrm_heap_fewshot, prompt="high_level_task", max_task_iters=10, max_policy_iters=10, task_debug=False, policy_debug=False, task_verbose=2, policy_verbose=2)


call_llm_fn = lambda prompt: call_llm(prompt, model_type="text-davinci-003")
policy_types = ["flat_zeroshot", "heap_zeroshot", "flat_fewshot", "heap_fewshot"]
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = f"data/eval/airlinecrm/{timestr}.csv"

idx = 0
for index, row in df_problems.iterrows():
    data = row.to_dict()
    for policy_type in policy_types:
        # idx = idx + 1
        # if idx <= 67+24:
        #     continue
        data['policy'] = policy_type
        env = AirlineCRMEnvironmentWrapper(context=row['context'], scenario=row['scenario'], max_browser_rows=200, max_steps=env_max_steps[row['task']])
        policy = get_policy(policy_type=policy_type, call_llm_fn=call_llm_fn, env=env)
        
        # Act
        policy.act()
        env.close()
        
        # Add success, task progress, excess actions to env()
        metrics = env.eval_metrics()
        for key, value in metrics.items():
            data[key] = value
		
        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        print(df)
        df.to_csv(filename, index=False)
        
    
df.to_csv(filename, index=False)
import pdb; pdb.set_trace()
