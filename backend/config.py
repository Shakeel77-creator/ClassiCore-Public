import os

# Absolute path to ClassiCore root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RESOURCE_DIR = os.path.join(DATA_DIR, "resources")

# Files
WORD_FREQ_PATH = os.path.join(RESOURCE_DIR, "word_freq.json")
EMBEDDINGS_FILE = os.path.join(RESOURCE_DIR, "unspsc_embeddings.pkl")
DB_PATH = os.path.join(DATA_DIR, "unspsc.db")
UNSPSC_EXCEL_PATH = os.path.join(DATA_DIR, "raw", "UNSPSC-Classification-Codes.xlsx")

# Model
ACTIVE_MODEL = "Granite"
#ACTIVE_MODEL = "Ollama"

