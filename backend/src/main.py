import os
import re
import sys
import time
import json
from backend.src.prompt_engine import build_prompts
from backend.llm.model_selector import predict_unspsc
from backend.src.unspsc_sqlite_search import SQLiteSearch
from utils.token_utils import get_search_tokens
from utils.phrase_utils import split_input_phrases
from backend.config import WORD_FREQ_PATH, DB_PATH


sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))

SQLiteSearch.load_db_to_memory(DB_PATH)

with open(WORD_FREQ_PATH, "r") as f:
    WORD_FREQ = json.load(f)

def classify_product(product_name: str):
    """
    Classifies a product using narrowing + LLM, or falls back to semantic suggestions.
    Handles compound phrases using `split_input_phrases`.
    """
    phrases = split_input_phrases(product_name)  # 👈 splitting happens here
    all_results = []

    for phrase in phrases:
        search_tokens, explanation = get_search_tokens(phrase, WORD_FREQ)
        print(f"🔍 Tokens for DB search (Phrase: '{phrase}'): {search_tokens}")

        search_result = SQLiteSearch.search_unspsc_sqlite(DB_PATH, tuple(search_tokens), word_freq=WORD_FREQ)

        # Fallback mode — do not call LLM
        if search_result["type"] == "semantic_fallback":
            print(f"\n⚠️ No direct match for '{phrase}'. Here are semantic suggestions:\n")
            for i, (name, code, score) in enumerate(search_result["suggestions"], start=1):
                print(f"{i}. {name} → {code} (Confidence: {score})")
            continue  # skip LLM for this phrase

        # Normal narrowed results — proceed with prompt + LLM
        narrowed_results = search_result["results"]
        prompts = build_prompts([phrase], narrowed_results)

        for subphrase, prompt in prompts:
            print(f"\n📤 Prompt for: {subphrase}\n{prompt}")
            start_time = time.time()
            output = predict_unspsc(prompt)
            end_time = time.time()

            match = re.search(r"\b\d{8}\b", output)
            predicted_code = match.group() if match else None

            # 🧠 NEW: Lookup the matched Name
            matched_name = SQLiteSearch.lookup_name_by_code(predicted_code) if predicted_code else None

            all_results.append({
                "input_phrase": subphrase,
                "predicted_code": predicted_code,
                "matched_name": matched_name,     # ✅ Added
                "elapsed": round(end_time - start_time, 2),
                "raw_output": output
            })

    return all_results

# Manual test
if __name__ == "__main__":
    product_name = "Shakeel Frozen giant yellow improved shallots Shiffan"
    begin = time.time()
    results = classify_product(product_name)

    if results:
        for result in results:
            print(f"✅ Phrase: {result['matched_name']} → Code: {result['predicted_code']}")
            print(f"⏱️ Time: {result['elapsed']}s | Raw Output: {result['raw_output']}\n")

        print(f"⏱️ Total Time: {round(time.time() - begin, 2)} seconds")
