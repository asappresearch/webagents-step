import pandas as pd
import openai
import os


from webactions_lm.utils.llm import call_generic_llm
from webactions_lm.prompt.processing import conversation_generator

openai.api_key = os.environ.get('OPENAI_API_KEY')
model_type = "gpt-3.5-turbo" # gpt-4, text-davinci-003, gpt-3.5-turbo
base_prompt = getattr(conversation_generator, "conversation_generator")

# Load a set of demonstrations
# Assume that one CSV corresponds to a set of episodes, and we will compute rollouts for each episode
#columns=['episode', 'time_step', 'context', 'url', 'browser_content', 'action'])
df_demo = pd.read_csv(f'data/demos/liveweb/flight_demos_across_uis.csv')
groups = df_demo.groupby('episode') # group the DataFrame by 'episode'

multiplier = 5
augmented_episode = 0
df_augmented = pd.DataFrame(columns=['context', 'url', 'episode', 'time_step', 'browser_content', 'action'])
for episode, df_episode in groups:
    context = df_episode.iloc[0]['context']
    url = df_episode.iloc[0]['url']
    for _ in range(multiplier):
        prompt = base_prompt
        prompt = prompt.replace("{input}", context)
        augmented_context = call_generic_llm(prompt, model_type=model_type)
        for _, row in df_episode.iterrows():
            row_augmented = pd.DataFrame({'context': [augmented_context],'url': [url], 'episode': [augmented_episode], 'time_step': [row['time_step']], 'browser_content': [row['browser_content']],'action': [row['action']]})
            df_augmented = pd.concat([df_augmented, row_augmented], ignore_index=True)
        augmented_episode = augmented_episode +1
            
import pdb; pdb.set_trace()
df_augmented.to_csv(f'data/demos/liveweb/flight_demos_across_uis_augmented.csv', index=False)