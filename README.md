# 🧠 Fact Generator

Fine-tune a small language model (GPT-2 or Phi-2) on a list of simple, newline-separated "facts". Generate new facts via a local web interface, retrain the model, and explore generation settings—all from your own machine.

---

## 📦 What’s Included

- `facts.txt` – Your dataset (one fact per line)
- `prepare_dataset.py` – Converts `facts.txt` into model-ready format
- `train_fact_model.py` – Trains the model (GPT-2 or Phi-2)
- `fact_server.py` – Runs a FastAPI server for generation, retraining, stats
- `index.html` – Minimal web UI for fact generation and model control
- `model-config.json` – Touch this file to trigger a live reload
- Setup scripts: `setup.sh`, `setup.ps1`, `retrain.sh`, `retrain.ps1`
- Docker support: `Dockerfile`, `docker-compose.yml`

---

## 🧰 Requirements

- Python 3.10+
- pip or Docker
- A GPU is recommended (see below)

---

## ⚙️ Supported Hardware

### ✅ NVIDIA GPU (CUDA)

Fully supported. Used automatically if detected.

### 🟠 AMD GPU (ROCm/CPU)

- This setup automatically falls back to CPU if CUDA is unavailable.
- Compatible with ROCm-based PyTorch builds, but does not require them.
- All functionality works on CPU, but will be **slower**, especially for Phi-2.

Verify which device is in use:
```python
print("Using device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")
```

---

## 🪟 Windows Setup

### 🔧 Without Docker (Command Line)

1. Run PowerShell:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   .\setup.ps1
   ```

2. Activate the virtual environment:
   ```powershell
   .env\Scripts\Activate.ps1
   ```

3. Train and run:
   ```powershell
   python prepare_dataset.py
   python train_fact_model.py
   python fact_server.py
   ```

4. Open `index.html` in your browser.

---

### 🐳 With Docker

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Build and run:
   ```powershell
   docker-compose up --build
   ```

3. Open `index.html` in your browser.

---

## 🐧 Linux Setup

### 🔧 Without Docker (Command Line)

1. Set up the environment:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   source venv/bin/activate
   ```

2. Train and run:
   ```bash
   python prepare_dataset.py
   python train_fact_model.py
   python fact_server.py
   ```

3. Open `index.html` in your browser.

---

### 🐳 With Docker

1. Build and run:
   ```bash
   docker-compose up --build
   ```

2. Open `index.html` in your browser.

---

## 🧪 Features

- 🔁 Live reload after training (no restart needed)
- 💬 Generate new facts from custom prompts
- 📈 Live logs from retraining (via server-sent events)
- 🌓 Dark-mode web UI (zero dependencies)
- 🔧 Choose model (`gpt2` or `phi2`) before training
- 🧠 Use sliders for temperature, token count, and more (optional extensions)
- 🖥 Works with NVIDIA GPUs, AMD GPUs (ROCm), or CPU fallback

---

## ✅ Usage Tips

- To add new facts: edit `facts.txt`, then click **Retrain** in the UI
- To change model: set `MODEL_TYPE=gpt2` or `MODEL_TYPE=phi2` in the environment or UI
- To force reload manually: touch `model-config.json` or click **Reload** in the UI
- To reset output: refresh the browser or clear the UI fields

---

## ⚠️ Notes

- Phi-2 training on CPU may take hours to complete—use GPT-2 if resources are limited
- Checkpoints are saved to `./fact-model/`
- You can change the training cadence using OS-level scheduling (e.g. `cron`, `Task Scheduler`)

---

Enjoy generating your own knowledge base! 🧠✨
