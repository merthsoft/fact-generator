FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Pre-copy requirements to cache pip layer
COPY requirements.txt .

# Install Python dependencies first to leverage Docker caching
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Preload models to prevent runtime downloads (optional)
RUN python -c "from transformers import AutoTokenizer, AutoModelForCausalLM;     AutoTokenizer.from_pretrained('gpt2'); AutoModelForCausalLM.from_pretrained('gpt2')"

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "fact_server.py"]
