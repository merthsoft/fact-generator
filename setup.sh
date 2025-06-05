#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install torch transformers datasets accelerate peft bitsandbytes fastapi uvicorn watchdog
