# backend/src/services/classify_service.py

import os
import re
import time
import json
from backend.src.unspsc_sqlite_search import SQLiteSearch
from backend.src.prompt_engine import PromptEngine
from backend.llm.model_selector import predict_unspsc
from backend.src.utils.token_utils import get_search_tokens
from backend.src.utils.phrase_utils import split_input_phrases
from backend.config import WORD_FREQ_PATH, DB_PATH
from backend.config import ACTIVE_MODEL

class ClassifyService:
    def __init__(self):
        # 🧠 Load once during service initialization
        SQLiteSearch.load_db_to_memory(DB_PATH)

        with open(WORD_FREQ_PATH, "r") as f:
            self.word_freq = json.load(f)

    def classify_product(self, product_name: str):
        """
        Classifies a product using narrowing + LLM, or falls back to semantic suggestions.
        """
        phrases = split_input_phrases(product_name)
        all_results = []

        for phrase in phrases:
            search_tokens, explanation = get_search_tokens(phrase, self.word_freq)
            print(f"🔍 Tokens for DB search (Phrase: '{phrase}'): {search_tokens}")

            search_result = SQLiteSearch.search_unspsc_sqlite(DB_PATH, tuple(search_tokens), word_freq=self.word_freq)

            if search_result["type"] == "semantic_fallback":
                suggestions = search_result["suggestions"]

                if suggestions and suggestions[0][2] >= 0.9:
                    # Confidence is high — return only the top suggestion
                    name, code, score = suggestions[0]
                    all_results.append({
                        "input_phrase": phrase,
                        "predicted_code": code,
                        "matched_name": name,
                        "elapsed": 0.0,
                        "confidence": f"Semantic match with confidence {score}",
                        "source": "Semantic Search"  # ✅ Marked fallback
                    })
                else:
                    # Confidence lower — return all fallback suggestions
                    for name, code, score in suggestions:
                        all_results.append({
                            "input_phrase": phrase,
                            "predicted_code": code,
                            "matched_name": name,
                            "elapsed": 0.0,
                            "confidence": score,
                            "source": "Semantic Search"  # ✅ Marked fallback
                        })
                continue

            narrowed_results = search_result["results"]
            prompts = PromptEngine.build_prompts([phrase], narrowed_results)

            for subphrase, prompt in prompts:
                print(f"\n📤 Prompt for: {subphrase}\n{prompt}")
                start_time = time.time()
                output = predict_unspsc(prompt)
                end_time = time.time()

                match = re.search(r"\b\d{8}\b", output)
                predicted_code = match.group() if match else None
                matched_name = SQLiteSearch.lookup_name_by_code(predicted_code) if predicted_code else None

                all_results.append({
                    "input_phrase": subphrase,
                    "predicted_code": predicted_code,
                    "matched_name": matched_name,
                    "elapsed": round(end_time - start_time, 2),
                    "raw_output": output,
                    "source": ACTIVE_MODEL  # ✅ Mark as LLM
                })

        return all_results
