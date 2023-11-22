import hydra
import os
import pandas as pd
from termcolor import colored

from webactions_lm.environment.liveweb import LiveWebEnvironmentWrapper


@hydra.main(config_path="../../config/liveweb/", config_name="flight_demos_across_uis")
def collect_demo(cfg):
    contexts = cfg.contexts
    num_episodes = cfg.num_episodes
    urls = cfg.urls
    save_dir = cfg.save_dir

    output_file = f"{save_dir}/flight_demos_across_uis.csv"
    if os.path.isfile(output_file):
        df = pd.read_csv(output_file)
    else:
        df = pd.DataFrame(
            columns=['context', 'url', 'episode', 'time_step', 'browser_content', 'action'])
        
    for context in contexts:
        for url in urls:
            env = LiveWebEnvironmentWrapper(context=context, url=url, max_browser_rows=1000)
            for episode in range(0, num_episodes):
                time_step = 0
                while True:
                    browser_content = env.observation()
                    print("==" * 60)
                    print(colored(context, "red"))
                    print("==" * 60)
                    print(colored(browser_content, "cyan"))
                    print("==" * 60)
                    print(
                        'Your action? Choose between {CLICK <ID>, TYPE <ID> "TEXT", DONE}')

                    action = input()

                    def is_done(obs, action): return (action == "DONE")
                    if is_done(browser_content, action):
                        break

                    row = pd.DataFrame({'context': [context],
                                        'url': [url],
                                        'episode': [episode],
                                        'time_step': [time_step],
                                        'browser_content': [browser_content],
                                        'action': [action]})

                    df = pd.concat([df, row], ignore_index=True)

                    env.step(action)
                    time_step = time_step + 1

                env.reset()

            env.close()

            print(f"Saving demo data to {output_file}")
            df.to_csv(output_file, index=False)

if __name__ == "__main__":
    collect_demo()