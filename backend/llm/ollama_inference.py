# ollama_inference.py
import requests

def predict_unspsc(prompt: str) -> str:
    print("🧠 Sending prompt to Ollama...")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",  # You can change this later
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    output = response.json()
    return output["response"].strip()
