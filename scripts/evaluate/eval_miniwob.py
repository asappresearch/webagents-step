import os
import pandas as pd
import time
import re
import argparse
import itertools
from tqdm import tqdm

import os
import sys
import argparse
from typing import List
import shutil

import openai

from webagents_step.utils.data_prep import *
from webagents_step.agents.prompt_agent import PromptAgent
from webagents_step.agents.step_agent import StepAgent
from webagents_step.prompts.miniwob import flat_fewshot_template, step_fewshot_template
from webagents_step.environment.miniwob import MiniWoBEnvironmentWrapper

openai.api_key = os.environ.get("OPENAI_API_KEY")

def run():
    parser = argparse.ArgumentParser(
        description="Only the config file argument should be passed"
    )
    parser.add_argument(
        "--config", type=str, required=True, help="yaml config file location"
    )
    args = parser.parse_args()
    with open(args.config, "r") as file:
        config = DotDict(yaml.safe_load(file))
    
    dstdir = f"{config.logdir}/{time.strftime('%Y%m%d-%H%M%S')}"
    os.makedirs(dstdir, exist_ok=True)
    shutil.copyfile(args.config, os.path.join(dstdir, args.config.split("/")[-1]))
    random.seed(42)

    tasks = config.env.tasks
    seeds = range(config.env.start_seed, config.env.end_seed)
    sampled_seeds = (
        random.sample(seeds, config.env.num_samples_per_task)
        if (config.env.num_samples_per_task > 0)
        else seeds
    )

    #####
    # Initialize agent
    #####        
    if config.agent.type == "step":
        action_to_prompt_dict = {k: v for k, v in step_fewshot_template.__dict__.items() if isinstance(v, dict)}
        low_level_action_list = config.agent.low_level_action_list
        agent_init = lambda: StepAgent(
            root_action = config.agent.root_action,
            action_to_prompt_dict = action_to_prompt_dict,
            low_level_action_list = low_level_action_list,
            max_actions=config.env.max_env_steps,
            verbose=config.verbose,
            logging=config.logging,
            debug=config.debug,
            model=config.agent.model_name,
            prompt_mode=config.agent.prompt_mode,
        )
    elif config.agent.type == "flat_fewshot":
        agent_init = lambda: PromptAgent(
            prompt_template=flat_fewshot_template.flat_fewshot_agent,
            model=config.agent.model_name,
            prompt_mode=config.agent.prompt_mode,
            max_actions=config.env.max_env_steps,
            verbose=config.verbose,
            logging=config.logging,
            debug=config.debug,
        )
    else:
        raise NotImplementedError(f"{config.agent.type} not implemented")

    #####
    # Evaluate
    #####

    for task_seed_pair in tqdm(itertools.product(tasks, sampled_seeds)):
        task, seed = task_seed_pair
        env = MiniWoBEnvironmentWrapper(
            task=task,
            seed=seed,
            max_browser_rows=config.env.max_browser_rows,
            max_steps=config.env.max_env_steps,
            headless=config.env.headless,
        )
        agent = agent_init()
        objective = env.get_objective()
        status = agent.act(objective=objective, env=env)
        env.close()

        if config.logging:
            log_file = os.path.join(dstdir, f"{task}_{seed:03d}.json")
            log_data = {
                "task": task,
                "seed": seed,
                "model": config.agent.model_name,
                "trajectory": agent.get_trajectory(),
            }
            summary_file = os.path.join(dstdir, "summary.csv")
            summary_data = {
                "task": task,
                "seed": seed,
                "model": config.agent.model_name,
                "logfile": re.search(r"/([^/]+/[^/]+\.json)$", log_file).group(1),
            }
            summary_data.update(status)
            log_run(
                log_file=log_file,
                log_data=log_data,
                summary_file=summary_file,
                summary_data=summary_data,
            )
    
if __name__ == "__main__":
    run()
