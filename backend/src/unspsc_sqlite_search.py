import sqlite3
import os
from backend.src.embedding_engine import run_semantic_search

class SQLiteSearch:
    # Whether to use in-memory DB (recommended for prod)
    USE_MEMORY_DB = True
    MEM_CONN = None  # Singleton connection for in-memory DB

    @staticmethod
    def load_db_to_memory(db_path: str):
        global MEM_CONN
        file_conn = sqlite3.connect(db_path)
        MEM_CONN = sqlite3.connect(":memory:", check_same_thread=False)
        file_conn.backup(MEM_CONN)
        file_conn.close()
        print("🧠 SQLite loaded into memory.")

    @staticmethod
    def is_single_word(tokens: tuple[str]) -> bool:
        """Detect if user input is a single word based on tokens."""
        return len(tokens) == 1

    @staticmethod
    def search_unspsc_sqlite(db_path: str, tokens: tuple[str], word_freq: dict, min_results: int = 10):
        if not tokens:
            print("❌ No valid tokens provided.")
            return []

        # Filter only known tokens first
        valid_tokens = [t for t in tokens if t in word_freq]

        # Now sort them by rarity
        sorted_tokens = sorted(valid_tokens, key=lambda t: word_freq[t])
        print("🔍 Sorted by rarity:", sorted_tokens)

        global MEM_CONN
        if MEM_CONN is None:
            raise Exception("❌ MEM_CONN is not initialized. Call load_db_to_memory() first.")

        cursor = MEM_CONN.cursor()
        results = set()
        where_clauses = []

        for token in sorted_tokens:
            where_clauses.append(f"LOWER(Name) LIKE '%{token.lower()}%'")
            query = f"""
                SELECT Name, Code
                FROM unspsc_master
                WHERE {" AND ".join(where_clauses)}
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            results = set(rows)

            print(f"🔍 After adding '{token}': {len(results)} results.")

            # Check if enough results
            if len(results) < min_results:
                break  # Good enough match, stop here
                
        if (len(results) == 0) or (len(results) > min_results) or (len(valid_tokens) <= 2 and (len(results) <= 2)):
            print("⚠️ No LIKE results found. Falling back to Semantic Search.")
            matches = run_semantic_search(' '.join(sorted_tokens), top_k=5)
            suggestions = []

            for title, score in matches:
                cursor.execute("SELECT Code FROM unspsc_master WHERE Name = ?", (title,))
                row = cursor.fetchone()
                if row:
                    suggestions.append((title, row[0], round(score, 3)))

            print("✅ Semantic suggestions for manual selection:")
            for i, (name, code, score) in enumerate(suggestions, start=1):
                print(f"{i}. {name} → {code} (Score: {score})")

            return {
                "type": "semantic_fallback",
                "suggestions": suggestions
            }

        return {
            "type": "narrowed",
            "results": list(results)
        }

    @staticmethod
    def lookup_name_by_code(code: str):
        """
        Lookup Product Name by UNSPSC Code from SQLite.
        """
        global MEM_CONN
        if MEM_CONN is None:
            raise Exception("❌ MEM_CONN is not initialized. Call load_db_to_memory() first.")

        cursor = MEM_CONN.cursor()
        cursor.execute("SELECT Name FROM unspsc_master WHERE Code = ?", (code,))
        row = cursor.fetchone()
        return row[0] if row else None
