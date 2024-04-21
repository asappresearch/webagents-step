# SteP: Stacked LLM Policies for Web Actions

## Installation

To set up the project, clone the repository and create a virtual environment:

```bash
cd webactions-lm
pyenv virtualenv webactions-lm
pyenv activate webactions-lm
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Install miniwob from https://github.com/Farama-Foundation/miniwob-plusplus. Use commit 43bd1fe. 

## Usage

To run miniwob evaluation:
```bash
python scripts/miniwob/eval_miniwob.py
```

<!-- ## Notes
* HeaP is interchangably referred to as PAW at some places. We'll fix that for consistency.
* We'll add usage examples for the remaining environments in the full code release. For now, one can find their low-level implementation details under src/ and evaluation metrics under analysis/notebooks. -->
