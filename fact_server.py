device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  # May be ROCm or CPU
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32).to(device).eval()
inputs = tokenizer(prompt + "\n", return_tensors="pt")