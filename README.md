# SteP: Stacked LLM Policies for Web Actions

Paper link: [https://arxiv.org/abs/2310.03720](https://arxiv.org/abs/2310.03720)

## Installation

To set up the project, clone the repository and create a virtual environment:

```bash
cd webagents-step
pyenv virtualenv webagents-step
pyenv activate webagents-step
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## WebArena Evaluation

### WebArena Results

We break down the success rates across different websites and provide links to the trajectory logs below, containing the observations, model predictions, and evaluator outputs for each task.

We are generating new runs with the `gpt-4-turbo-2024-04-09` model and latest WebArena code (last commit May 29, 2024) and will be updating the table below,

| Website | Number of tasks              | Success Rate | Trajectory Logs             |
|---------|--------------------|--------------|------------------|
| Reddit  | 106 | 59.4%        | [logs](https://drive.google.com/drive/folders/1Ek9cMz344tKXbEchakPyPXoTU14FYSlm?usp=share_link) |
| Map  | 109 | 30.3%       | [logs](https://drive.google.com/drive/folders/1V7c122QKNAIVdbskLFNwTJcwILGIf_kS?usp=share_link) |
| Gitlab  | 180 | 31.7%       | [logs](https://drive.google.com/drive/folders/1znkg8aQoEVLTvSyQ8iebb_bsOJL2DrKl?usp=share_link) |
| Shopping  |  | TBD       | |
| Shopping admin (CMS)  | 182 |   24.2%   | [logs](https://drive.google.com/drive/folders/1quti9851rBO49alYYL9C1NZNcpRI_Cg-?usp=share_link) |
| Multisite  | 48 |   12.5%    | [logs](https://drive.google.com/drive/folders/1JmvrY1Ys_bHHY8eQmJocnyZGiPeG7BpV?usp=share_link) |


### Installing WebArena
Install WebArena from [WebArena github repository](https://github.com/web-arena-x/webarena). This code uses the last commit 4c741b4b20a3e183836e58f383f9be1785248160 on May 29, 2024.

Generate test data configs:
```bash
python scripts/generate_test_data.py
```
You will see `*.json` files generated in config_files/ folder. Copy these over to a `tasks/webarena` directory in the `webagents-step/` root directory.

### Running Evaluation

To run WebArena evaluation:
```bash
python scripts/evaluate/eval_webarena.py --config configs/webarena/eval_openai_agent.yml
```

Important:
* Set up each website as a docker as listed in [WebArena instructions](https://github.com/web-arena-x/webarena/blob/main/environment_docker/README.md)
* Reset the website state before running an evaluation. This matters since the initial state of the website affects the success of the task.
* For Reddit tasks, there is a rate limit on making more than 3 posts in an hour. You need to add a sleep of 21 minutes before every new task. This can be done by adding `time.sleep(1260)` inside the for loop in `eval_webarena.py`

## MiniWoB++ Evaluation

### Installing MiniWob++
Install MiniWoB++ from [this repository](https://github.com/Farama-Foundation/miniwob-plusplus). Use commit 43bd1fe.

### Running Evaluation

To run MiniWoB++ evaluation:
```bash
python scripts/evaluate/eval_miniwob.py --config configs/miniwob/eval_openai_agent.yml
```

## Contact
This project is still in active development. For any questions or issues, please contact us at [psodhi@asapp.com](mailto:psodhi@asapp.com).