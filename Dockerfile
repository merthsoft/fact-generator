FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python3-pip git &&     pip3 install --upgrade pip &&     pip3 install torch transformers datasets accelerate peft bitsandbytes fastapi uvicorn

WORKDIR /workspace

CMD [ "bash" ]
