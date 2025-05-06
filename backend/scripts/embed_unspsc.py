# src/embed_unspsc.py

import sqlite3
import os
import pickle
from sentence_transformers import SentenceTransformer
from backend.config import DB_PATH, EMBEDDINGS_FILE

# Connect to DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT Name FROM unspsc_master")
rows = cursor.fetchall()
titles = [row[0] for row in rows]
conn.close()

print(f"📚 Loaded {len(titles)} UNSPSC titles.")

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(titles, show_progress_bar=True)

# Save to pickle
with open(EMBEDDINGS_FILE, "wb") as f:
    pickle.dump({
        "titles": titles,
        "embeddings": embeddings
    }, f)

print(f"✅ Saved embeddings to {EMBEDDINGS_FILE}")
