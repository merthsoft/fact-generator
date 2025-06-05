venv\Scripts\Activate.ps1
python prepare_dataset.py
python train_fact_model.py
(Get-Item "model-config.json").LastWriteTime = Get-Date
