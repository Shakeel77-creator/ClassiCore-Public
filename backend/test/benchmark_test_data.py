import os
import time
import pandas as pd
from backend.src.main import classify_product
from backend.config import PROJECT_ROOT

INPUT_CSV = os.path.join(PROJECT_ROOT, "backend", "test", "Sample_Multi-domain_User_Input_Test_Data.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "backend", "test")
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "benchmark_results.csv")

def ensure_output_dir(path: str):
    os.makedirs(path, exist_ok=True)

def run_benchmark(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)

    title_col = next(col for col in df.columns if "product" in col.lower())
    expected_col = next(col for col in df.columns if "expected" in col.lower())

    results = []
    correct = 0
    total_time = 0

    print(f"\n🧪 Running benchmark on {len(df)} samples...\n")

    for idx, row in df.iterrows():
        product = str(row[title_col])
        expected = str(row[expected_col]).strip()

        try:
            all_results = classify_product(product)

            if not all_results:
                raise ValueError("No classification result returned")

            top = all_results[0]
            predicted = top.get("predicted_code", "ERROR")
            duration = top.get("elapsed", 0)

            print(f"{idx+1}. 🛒 {product[:60]}...")
            print(f"   🔄 Predicted: {predicted} | Expected: {expected}")
            print(f"   ⏱️ Time: {duration}s\n")

            correct += int(predicted == expected)
            total_time += duration

            results.append({
                "Product": product,
                "Expected": expected,
                "Predicted": predicted,
                "Correct": predicted == expected,
                "Time (s)": round(duration, 3)
            })

        except Exception as e:
            print(f"{idx+1}. ❌ Error classifying: {product[:60]} | {e}\n")
            results.append({
                "Product": product,
                "Expected": expected,
                "Predicted": "ERROR",
                "Correct": False,
                "Time (s)": 0
            })

    accuracy = round((correct / len(results)) * 100, 2)
    avg_time = round(total_time / len(results), 3)

    print(f"\n🎯 Final Accuracy: {accuracy}%")
    print(f"⏱️ Avg Time per sample: {avg_time}s")

    ensure_output_dir(os.path.dirname(output_csv))
    pd.DataFrame(results).to_csv(output_csv, index=False)
    print(f"\n📁 Benchmark results saved to: {output_csv}")

if __name__ == "__main__":
    run_benchmark(INPUT_CSV, OUTPUT_CSV)
