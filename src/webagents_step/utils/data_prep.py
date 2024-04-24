import os
import json
import pandas as pd
import random
import yaml
import copy
import numpy as np

class yamlConfig:
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = yamlConfig(value)
            setattr(self, key, value)

class DotDict:
    """access dictionary attributes with dot notation"""
    def __init__(self, dictionary):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                value = DotDict(value)
            setattr(self, key, value)
    
    def to_dict(self):
        regular_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, DotDict):
                regular_dict[key] = value.to_dict()
            else:
                regular_dict[key] = value
        return regular_dict
    
    def has_key(self, key):
        """Check if the DotDict has a specific key"""
        return hasattr(self, key)
    
#####
# Dataset processing functions
#####

def split_list_by_proportion(proportion, original_list):
    list_size = len(original_list)
    first_list_size = int(proportion * list_size)
    shuffled_list = copy.copy(original_list)
    random.shuffle(shuffled_list)
    first_list = shuffled_list[:first_list_size]
    second_list = shuffled_list[first_list_size:]
    return first_list, second_list


def examples_to_prompts(data_config, json_df, prompt_template, inference):
    all_prompt_strings = []
    for idx, row in json_df.iterrows():
        try:
            # read samples
            json_filepath = os.path.join(data_config.basedir, str(row.logfile))
            with open(json_filepath,'r') as json_file:
                example_json = json.load(json_file)
            all_prompt_strings.extend(convert_example_to_prompts(example_json, data_config, prompt_template, inference))
        except FileNotFoundError:
            print(f"File {data_config.basedir}/{row.logfile} not found. Skipping ...")
            continue
            
    return all_prompt_strings

def convert_example_to_prompts(example_json, data_config, prompt_template, inference):
    filled_prompt_strings = []
    previous_actions = []
    for step_ind, step in enumerate(example_json["trajectory"]):
        # Fill in prompt components
        prompt_components = copy.deepcopy(prompt_template)        
        prompt_components["input"] = prompt_components["input"].format(
            objective = step["objective"], 
            observation = step["observation"], 
            url = step["url"], 
            previous_actions = "\n".join([str(step) for step in step["previous_actions"][-data_config.action_lookback:] if step is not None]) if "previous_actions" in step else "\n".join([str(action) for action in previous_actions[-data_config.action_lookback:] if action is not None])
        )
        previous_actions.append(step["action"])

        prompt_components["response"] = convert_actions_and_reasons_to_response(step["reason"], step["action"])
        filled_prompt_strings.append(create_prompt(prompt_components, inference=inference))
    return filled_prompt_strings

def convert_actions_and_reasons_to_response(reasons, actions):
    response = f"""
REASON:
{reasons}
ACTION:
{actions}
"""
    return response

def create_prompt(prompt_components, inference=False):
    #If inference mode, do not fill in the response
    if inference:
        prompt_template = """
<s>[INST] <<SYS>>
{instruction}
<</SYS>>

{input} [/INST]"""
        return prompt_template.format(instruction = prompt_components["instruction"],
                                  input = prompt_components["input"])
    else:
        prompt_template = """
<s>[INST] <<SYS>>
{instruction}
<</SYS>>

{input} [/INST] {response} </s>
"""
        return prompt_template.format(instruction = prompt_components["instruction"],
                                  input = prompt_components["input"],
                                  response = prompt_components["response"])

def log_run(log_file, log_data, summary_file=None, summary_data=None, json_indent=4, verbose=1):
    """
    Logs demo data to a JSON file and optionally updates a summary CSV file.
    """
    # Write log data to JSON file
    with open(log_file, 'w') as json_file:
        json.dump(log_data, json_file, indent=json_indent)
    if verbose:
        print(f"Saved log to {log_file}")

    # If summary data and file path are provided, update the summary
    if summary_data and summary_file:
        if os.path.exists(summary_file):
            df_summary = pd.read_csv(summary_file)
        else:
            df_summary = pd.DataFrame()
        df_summary = pd.concat([df_summary, pd.DataFrame([summary_data])], ignore_index=True)
        df_summary.to_csv(summary_file, index=False)
        if verbose:
            print(f"Updated summary: {df_summary}")
        
        return df_summary