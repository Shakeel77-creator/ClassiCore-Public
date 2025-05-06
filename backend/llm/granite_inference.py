from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "ibm-granite/granite-3.2-2b-instruct"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

def predict_unspsc(prompt: str) -> str:
    # Format as chat message
    chat = [{"role": "user", "content": prompt}]
    formatted_prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

    inputs = tokenizer(formatted_prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=8,
        )

    # Slice off the prompt
    response = tokenizer.decode(
        outputs[0, inputs["input_ids"].shape[1]:],
        skip_special_tokens=True
    )
    return response.strip()

