import sqlite3
import pandas as pd
import json
import re
from collections import Counter
from backend.config import DB_PATH, WORD_FREQ_PATH

def tokenize(text: str):
    return re.findall(r'\b\w+\b', str(text).lower())

# Connect to SQLite and load all Commodity_Titles
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT Name FROM unspsc_master", conn)
conn.close()

# Tokenize all titles
all_tokens = []
for title in df["name"]:
    all_tokens.extend(tokenize(title))

# Count frequencies
word_freq = Counter(all_tokens)

# Save to disk
with open(WORD_FREQ_PATH, "w") as f:
    json.dump(word_freq, f, indent=2)

print("✅ word_freq.json generated!")
