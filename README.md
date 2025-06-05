# Fact Generator: Train Your Own GPT-2 or Phi-2 Model on Custom Facts

This project allows you to fine-tune a small language model (GPT-2 or Phi-2) on a newline-delimited list of "facts". It includes a simple web UI to test generation, trigger retraining, and inspect the model.

---

## 📁 Folder Contents

- `facts.txt` — Your list of facts (one per line).
- `train_fact_model.py` — Trains the model using your facts.
- `prepare_dataset.py` — Converts `facts.txt` into a dataset.
- `fact_server.py` — REST API for generation, retraining, and stats.
- `index.html` — Local web UI (open in browser).
- `model-config.json` — Triggers live model reloads when touched.
- `setup.ps1` / `setup.sh` — One-time environment setup.
- `retrain.ps1` / `retrain.sh` — Manual retraining helpers.
- `Dockerfile` / `docker-compose.yml` — Docker support.

---

## 🖥️ Windows Instructions

### 🔧 CLI Setup (no Docker)

1. Run PowerShell:
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   ./setup.ps1
   ```

2. Activate the environment:
   ```powershell
   venv\Scripts\Activate.ps1
   ```

3. Train and run:
   ```powershell
   python prepare_dataset.py
   python train_fact_model.py
   python fact_server.py
   ```

4. Open `index.html` in your browser.

### 🐳 Docker on Windows

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. Build the image:
   ```powershell
   docker build -t fact-model .
   ```

3. Start the server:
   ```powershell
   docker-compose up --build
   ```

4. Open `index.html` in your browser.

---

## 🐧 Linux Instructions

### 🔧 CLI Setup (no Docker)

1. Run setup:
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

### 🐳 Docker on Linux

1. Build the image:
   ```bash
   docker build -t fact-model .
   ```

2. Start the server:
   ```bash
   docker-compose up --build
   ```

3. Open `index.html` in your browser.

---

## 🧪 Features

- Live text generation using your trained model
- Prompt-based fact generation (e.g. "cats", "science")
- Full retraining with new facts or new model type
- Real-time retraining logs in UI (via SSE)
- Model reload without restart
- Web UI with dark mode

---

## 🔄 Tips

- To retrain: edit `facts.txt`, then click “Retrain” in the UI
- To change model: use dropdown in UI or set `MODEL_TYPE` env var (`gpt2` or `phi2`)
- To force reload: touch `model-config.json` or use `/reload` in the UI

---

## 📦 Notes

- GPU is required for training and serving
- Model checkpoints are saved in `fact-model/`
- Live model reload is based on file timestamp, not content

