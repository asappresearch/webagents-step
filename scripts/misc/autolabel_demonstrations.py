import pandas as pd
import openai
import os
from tqdm import tqdm

from webactions_lm.utils.llm import call_llm, add_latest_state_to_prompt
from webactions_lm.prompts.processing import autolabel

openai.api_key = os.environ.get('OPENAI_API_KEY')
model_type = "gpt-4" # gpt-4, text-davinci-003, gpt-3.5-turbo
verbose = True

# Load a demonstration
## List of (context, browser_content, action)
df = pd.read_csv('data/demonstrations.csv')

# Initialize dataframe with columns
# Context
# browser_content
# action
# timestep
# episode number

# Call labeller
## For every element of the list
### Feed context, browser_context, action to the prompt.
### Also add previous label
### Get current label
### Add to a dataframe row

base_prompt = getattr(autolabel, "autolabel_liveweb")

previous_label = ''
for index, row in tqdm(df.iterrows()):
    if (row['episode']> 0):
        break    
    prompt_values = {"{context}": row['context'], 
                  "{browser_content}": row['browser_content'][:10000], 
                  "{current_action}": row['action'],
                  "{previous_label}": previous_label}
    prompt = base_prompt
    for k, v in prompt_values.items():
        prompt = prompt.replace(k, v)

    response = call_llm(prompt, model_type=model_type)
    df.loc[index, 'label'] = response
    previous_label = response

df.to_csv('data/labeled_demonstrations.csv', index=False)