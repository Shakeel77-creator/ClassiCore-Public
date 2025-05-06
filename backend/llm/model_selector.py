# model_selector.py
from backend.config import ACTIVE_MODEL

if ACTIVE_MODEL == "Granite":
    from backend.llm.granite_inference import predict_unspsc
elif ACTIVE_MODEL == "Ollama":
    from backend.llm.ollama_inference import predict_unspsc
else:
    raise ValueError(f"Unsupported model: {ACTIVE_MODEL}")
