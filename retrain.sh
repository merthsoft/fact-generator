#!/bin/bash
source venv/bin/activate
python prepare_dataset.py
python train_fact_model.py
touch model-config.json
