import json
import os
import pandas as pd

# Lista completa de modelos, incluyendo baseline
MODELS = [
    "autonomous",
    "at_source",
    "custodian",
    "guided",
    "federated",
    "baseline"
]

def load_all_results():
    results_by_model = {}
    for model in MODELS:
        file = f"results_{model}.json"
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                results_by_model[model] = json.load(f)
        else:
            print(f" Warning: file not found: {file}")
    return results_by_model

def build_comparison_table(results_by_model):
    rows = []
    for query_index in range(len(next(iter(results_by_model.values())))):
        row = {"query_index": query_index + 1}
        row["query"] = results_by_model[MODELS[0]][query_index]["query"]

        for model in MODELS:
            result = results_by_model.get(model, [])[query_index]
            row[f"{model}_docs"] = result.get("retrieved_fragments", None)
            row[f"{model}_dps"] = result.get("dps_contributing", None)
            row[f"{model}_latency_ms"] = result.get("latency_ms", None)
            row[f"{model}_redundancy"] = result.get("redundancy_count", None)
            row[f"{model}_answer"] = result.get("generated_answer", "")[:300]
        rows.append(row)

    df = pd.DataFrame(rows)
    return df

def save_table(df, output_file="comparison_table.csv"):
    df.to_csv(output_file, index=False)
    print(f"\n Comparison table saved to {output_file}")

def main():
    results_by_model = load_all_results()
    df = build_comparison_table(results_by_model)

    pd.set_option("display.max_colwidth", 100)
    print("\n=== Comparison of Answers by Model and Query ===\n")
    display_cols = ["query_index", "query"] + [f"{m}_answer" for m in MODELS]
    print(df[display_cols].to_string(index=False))

    save_table(df)

if __name__ == "__main__":
    main()
