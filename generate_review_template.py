import csv
from queries import QUERIES

MODELS = [
    "autonomous",
    "at_source",
    "custodian",
    "guided",
    "federated",
    "baseline"
]

OUTPUT_FILE = "manual_review_template.csv"

def main():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_index", "query", "model", "relevance", "hallucination_risk", "traceability", "comments"])

        for idx, query in enumerate(QUERIES, start=1):
            for model in MODELS:
                writer.writerow([idx, query, model, "", "", "", ""])

    print(f"✅ Manual review template saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
