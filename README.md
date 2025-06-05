# Fact Model (GPT-2 or Phi-2) Fine-Tuning and Inference

This package allows you to fine-tune GPT-2 or Phi-2 on a newline-delimited list of "facts" and serve them through a FastAPI server.

---

## 🚀 Model Choice: GPT-2 vs Phi-2

Set the environment variable:

- `MODEL_TYPE=gpt2`
- `MODEL_TYPE=phi2`

---

## 🐳 Docker Setup

### Build the Docker Image
```bash
docker build -t fact-model .
```

### Run Fine-Tuning
```bash
docker run --gpus all --rm -v ${PWD}:/workspace -e MODEL_TYPE=gpt2 fact-model bash -c "python prepare_dataset.py && python train_fact_model.py"
```

### Start the Server
```bash
docker run --gpus all -v ${PWD}:/workspace -e MODEL_TYPE=gpt2 -p 8000:8000 fact-model python fact_server.py
```

---

## 🧱 Docker Compose Setup (Recommended)

### Start the Server
```bash
docker-compose up --build
```

### Run Fine-Tuning
```bash
docker-compose run retrain
```

---

## 🖥️ Local Linux Setup

Run:

```bash
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python prepare_dataset.py
python train_fact_model.py
python fact_server.py
```

---

## 📅 Cron Setup (Linux)

Add this line to your crontab (`crontab -e`):

```
0 3 * * 1 cd /path/to/your/project && ./retrain.sh >> cron.log 2>&1
```

This retrains every Monday at 3 AM.

---

## 📅 Windows Task Scheduler Setup

1. Open Task Scheduler
2. Create Basic Task → Set schedule
3. Action → Start a program:
   ```
   powershell.exe
   ```
4. Arguments:
   ```
   -ExecutionPolicy Bypass -File "C:\Path\To\retrain.ps1"
   ```

---

## 🔁 Auto-Reloading

The FastAPI server monitors `model-config.json`. When it's touched (e.g., via retrain), the model is automatically reloaded without restarting the server.

---

## 🧪 Example API Call

**POST** `http://localhost:8000/generate`
```json
{
  "prompt": "Fact:\n",
  "max_tokens": 32,
  "temperature": 1.0
}
```

---

## 📄 Files

- `facts.txt`: Your newline-delimited facts
- `setup.sh`, `setup.ps1`: Setup scripts
- `retrain.sh`, `retrain.ps1`: Retraining scripts
- `model-config.json`: Touch this file to trigger a model reload
