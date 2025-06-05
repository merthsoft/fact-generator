import os
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_from_disk
from peft import get_peft_model, LoraConfig, TaskType

model_type = os.getenv("MODEL_TYPE", "gpt2")
model_name = {
    "gpt2": "gpt2",
    "phi2": "microsoft/phi-2"
}[model_type]

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

dataset = load_from_disk("facts_dataset")
dataset = dataset.map(lambda x: tokenizer(x["text"], truncation=True, padding="max_length", max_length=64), batched=True)
dataset.set_format(type="torch", columns=["input_ids", "attention_mask"])

model = AutoModelForCausalLM.from_pretrained(model_name)

target_modules = ["c_attn"] if model_type == "gpt2" else ["q_proj", "v_proj"]
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=target_modules,
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_config)

training_args = TrainingArguments(
    output_dir="./fact-model",
    per_device_train_batch_size=4,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_dir="./logs",
    fp16=True,
    save_total_limit=2,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)
trainer.train()
model.save_pretrained("fact-model")
tokenizer.save_pretrained("fact-model")
