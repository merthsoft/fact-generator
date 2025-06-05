import os
import time
import threading
import subprocess
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

model_type = os.getenv("MODEL_TYPE", "phi2")
model_name = "fact-model"

model_lock = threading.Lock()
device = torch.device("cpu")  # AMD/ROCm fallback – forcing CPU usage
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device).eval()
last_modified = os.path.getmtime("model-config.json")

def reload_model():
    global model, tokenizer, last_modified
    with model_lock:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name).to(device).eval()
        last_modified = os.path.getmtime("model-config.json")

def watcher():
    global last_modified
    while True:
        time.sleep(5)
        try:
            mtime = os.path.getmtime("model-config.json")
            if mtime != last_modified:
                reload_model()
        except Exception:
            pass

threading.Thread(target=watcher, daemon=True).start()

class GenerateRequest(BaseModel):
    prompt: str = "Fact:"
    max_tokens: int = 32
    temperature: float = 1.0

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        with model_lock:
            prompt = f"Fact about {req.prompt.strip()}:" if req.prompt.strip().lower() != "fact:" else "Fact:"
            inputs = tokenizer(prompt + "\n", return_tensors="pt")
            output = model.generate(
                **inputs,
                max_new_tokens=req.max_tokens,
                temperature=req.temperature,
                do_sample=True,
                top_p=0.95
            )
            result = tokenizer.decode(output[0], skip_special_tokens=True)
            return {"text": result.strip()}
    except Exception as e:
        return {"error": str(e)}

@app.post("/reload")
def manual_reload():
    reload_model()
    return {"status": "Model reloaded"}

@app.get("/stats")
def stats():
    return {
        "model_type": model_type,
        "last_reload": time.ctime(last_modified),
    }

@app.get("/retrain-stream")
def retrain_stream(model_type: str = "phi2"):
    def event_stream():
        if not os.path.exists("train_fact_model.py"):
            yield "data: ERROR: Training script missing\n\n"
            return
        proc = subprocess.Popen(
            ["python", "train_fact_model.py"],
            env={**os.environ, "MODEL_TYPE": model_type},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in proc.stdout:
            yield f"data: {line.strip()}\n\n"
        proc.wait()
        os.utime("model-config.json", None)
        yield "event: done\ndata: Retrain complete\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")
