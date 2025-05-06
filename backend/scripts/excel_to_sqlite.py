import os
import pandas as pd
import sqlite3
from backend.config import DB_PATH, UNSPSC_EXCEL_PATH

# === Step 2: Sheet-to-column mapping ===
sheet_config = {
    "SEGMENT": ("SEGMENT", "SEGMENT DESCRIPTION"),
    "FAMILY": ("FAMILY", "FAMILY DESCRIPTION"),
    "CLASS": ("CLASS", "CLASS DESCRIPTION"),
    "COMMODITY": ("COMMODITY", "COMMODITY DESCRIPTION"),
}

unique_entries = set()

# === Step 3: Extract data from each sheet ===
for sheet, (code_col, name_col) in sheet_config.items():
    print(f"📄 Processing sheet: {sheet}")
    try:
        df = pd.read_excel(UNSPSC_EXCEL_PATH, sheet_name=sheet)
        for _, row in df.iterrows():
            name = str(row.get(name_col, "")).strip()
            code = str(row.get(code_col, "")).strip()
            if name and code:
                unique_entries.add((name, code))
    except Exception as e:
        print(f"❌ Error in sheet '{sheet}': {e}")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# === Step 4: Insert into SQLite ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS unspsc_master")
cursor.execute("""
CREATE TABLE unspsc_master (
    name TEXT NOT NULL,
    code TEXT NOT NULL,
    UNIQUE(name, code)
)
""")

cursor.executemany("INSERT OR IGNORE INTO unspsc_master (name, code) VALUES (?, ?)", list(unique_entries))
conn.commit()
conn.close()

# === Step 5: Summary ===
print(f"\n✅ Done! Flattened data saved to: {DB_PATH}")
print(f"📦 Total unique entries inserted: {len(unique_entries)}")
