import re

SAFE_SPLITTERS = [r"\band\b", r"\bor\b"]

def split_input_phrases(user_input: str) -> list[str]:
    """
    Splits input text by safe conjunctions (like 'and', 'or').
    Ensures:
      - Empty parts are removed
      - Leading/trailing spaces are trimmed
      - Original full input is always added back
    """
    pattern = "|".join(SAFE_SPLITTERS)
    parts = re.split(pattern, user_input, flags=re.IGNORECASE)
    
    phrases = [p.strip() for p in parts if p.strip()]
    
    full = user_input.strip()
    if full not in phrases:
        phrases.append(full)
    
    return phrases


# ✅ Manual Test Example
if __name__ == "__main__":
    sample = "Adhesives and Sealants"
    result = split_input_phrases(sample)
    print("🔍 Split Result:", result)
    # Expected: ['Adhesives', 'Sealants', 'Adhesives and Sealants']
