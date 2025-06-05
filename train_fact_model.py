import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling

model_type = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_type)

def load_dataset(file_path):
    return TextDataset(
        tokenizer=tokenizer,
        file_path=file_path,
        block_size=128
    )

dataset = load_dataset("prepared_facts.txt")

model = AutoModelForCausalLM.from_pretrained(model_type)

training_args = TrainingArguments(
    output_dir="./fact-model",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=2,
    logging_dir="./logs",
    logging_steps=100
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
)

trainer.train()

# Save the model and tokenizer
model.save_pretrained("fact-model")
tokenizer.save_pretrained("fact-model")
