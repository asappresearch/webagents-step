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

## External dependencies

### WebArena
Install WebArena from [this repository](https://github.com/web-arena-x/webarena).

Generate test data configs:
```bash
python scripts/generate_test_data.py
```
You will see `*.json` files generated in config_files/ folder. Copy these over to a tasks/webarena folder in the webagents-step/ root directory.

### MiniWob++
Install MiniWoB++ from [this repository](https://github.com/Farama-Foundation/miniwob-plusplus). Use commit 43bd1fe.


## Usage

To run WebArena evaluation:
```bash
python scripts/evaluate/eval_webarena.py --config configs/webarena/eval_openai_agent.yml
```

To run MiniWoB++ evaluation:
```bash
python scripts/evaluate/eval_miniwob.py --config configs/miniwob/eval_openai_agent.yml
```
