#!/bin/bash

# prepare the evaluation
# re-validate login information
mkdir -p ./.auth
python scripts/webarena/auto_login.py
