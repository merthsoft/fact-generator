import os
import json
import torch
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, StreamingResponse, JSONResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
import time

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_dir = "fact-model"
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    local_files_only=True
).to(device).eval()

tokenizer = AutoTokenizer.from_pretrained(
    model_dir,
    local_files_only=True
)

@app.get("/")
def root():
    return {"message": "Fact Generator API"}

@app.get("/generate")
def generate(prompt: str = "Fact: "):
    prompt = prompt or "Fact: "
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
                    inputs.input_ids,
                    max_new_tokens=50,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.8
                )
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"result": text}

@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    if os.path.exists("index.html"):
        return FileResponse("index.html")
    return HTMLResponse("<html><body><h1>UI not found</h1></body></html>", status_code=404)

@app.get("/reload")
def reload_model():
    global model, tokenizer
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    ).to(device).eval()
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    return {"status": "model reloaded"}

@app.get("/stats")
def get_stats():
    return {
        "model": model_dir,
        "device": str(device),
        "torch_cuda_available": torch.cuda.is_available(),
        "dtype": str(next(model.parameters()).dtype)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fact_server:app", host="0.0.0.0", port=8000, reload=False)
