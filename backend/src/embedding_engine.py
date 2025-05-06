from sentence_transformers import SentenceTransformer, util
import pickle
import os
from backend.config import EMBEDDINGS_FILE

# Load the embedding model (MiniLM lightweight)
EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# Load precomputed embeddings and corresponding names
if os.path.exists(EMBEDDINGS_FILE):
    with open(EMBEDDINGS_FILE, "rb") as f:
        embedding_data = pickle.load(f)
    UNSPSC_TITLES = embedding_data['titles']
    UNSPSC_EMBEDDINGS = embedding_data['embeddings']
else:
    UNSPSC_TITLES = []
    UNSPSC_EMBEDDINGS = None
    print("⚠️ Embedding file not found. Semantic search will not work.")

def run_semantic_search(user_input: str, top_k: int = 5):
    """
    Runs semantic search over the UNSPSC titles and returns top_k matches.
    """
    if UNSPSC_EMBEDDINGS is None or len(UNSPSC_EMBEDDINGS) == 0:
        raise ValueError("❌ Embeddings not loaded. Cannot perform semantic search.")

    query_embedding = EMBED_MODEL.encode(user_input, convert_to_tensor=True)
    search_results = util.semantic_search(query_embedding, UNSPSC_EMBEDDINGS, top_k=top_k)[0]

    matched = [(UNSPSC_TITLES[hit['corpus_id']], hit['score']) for hit in search_results]
    return matched
