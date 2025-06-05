from transformers import AutoTokenizer

model_name = "distilgpt2"
max_length = 1024

tokenizer = AutoTokenizer.from_pretrained(model_name)

with open("facts.txt", encoding="utf-8") as f_in, open("prepared_facts.txt", "w", encoding="utf-8") as f_out:
    for line in f_in:
        text = line.strip()
        if not text:
            continue

        # Encode full fact with "Fact: " prefix
        full_tokens = tokenizer.encode(f"Fact: {text}")
        if len(full_tokens) <= max_length:
            f_out.write(tokenizer.decode(full_tokens, clean_up_tokenization_spaces=True) + "\n")
        else:
            # Split into chunks
            for i, start in enumerate(range(0, len(full_tokens), max_length)):
                chunk = full_tokens[start:start + max_length]
                prefix = "Fact (continued): " if i > 0 else "Fact: "
                decoded = tokenizer.decode(chunk, clean_up_tokenization_spaces=True)
                # Ensure prefix is applied after decoding to avoid token mismatch
                f_out.write(f"{prefix}{decoded.strip()}\n")
