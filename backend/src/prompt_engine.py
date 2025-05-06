# backend/classifier-service/prompt_engine.py

import os
import pandas as pd
import json
from backend.config import WORD_FREQ_PATH

class PromptEngine : 
    # === Load frequency dictionary once ===
    with open(WORD_FREQ_PATH, "r") as f:
        WORD_FREQ = json.load(f)

    # === Main Function: Multi-prompt generator ===
    def build_prompts(phrases: list[str], narrowed_results: list = None) -> list[tuple[str, str]]:
        """
        Builds few-shot prompts for the given list of phrases using narrowed DB matches (if available).
        """
        prompts = []

        for phrase in phrases:
            examples = []

            # Use narrowed_results if provided (as few-shot examples)
            if narrowed_results:
                for name, code in list(narrowed_results)[:5]:  # Take top 5 examples
                    examples.append(f"- {name} → {code}")
            else:
                # Fallback default examples (optional)
                examples = [
                    "- Adhesives → 31201600",
                    "- Sealants → 31201700",
                    "- Laboratory tube sealants → 41122412",
                    "- Oil well sealants → 12163500",
                    "- Anti adhesives → 15121512"
                ]

            # Construct final prompt
            prompt = f"""You are a UNSPSC classification assistant. Given a product description, map it to the most appropriate UNSPSC code from the examples provided.
    Here are some examples:
    {chr(10).join(examples)}
    Now, based on the above patterns, return the exact 8-digit UNSPSC code that most precisely matches the product:
    "{phrase}"

    Only return the UNSPSC code with no explanation. Do not repeat the input or any explanation."""

            prompts.append((phrase, prompt))

        return prompts

