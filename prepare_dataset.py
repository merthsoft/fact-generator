from datasets import Dataset

with open("facts.txt") as f:
    lines = [line.strip() for line in f if line.strip()]
data = {"text": lines}
ds = Dataset.from_dict(data)
ds.save_to_disk("facts_dataset")
