import os
import time
import json
from queries import QUERIES
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI  

RESULTS_FILE = "results_baseline.json"

def main():
    results_log = []

    # Cargar clave desde .env
    load_dotenv()

    # Crear LLM con clave cargada desde entorno
    llm = ChatOpenAI(
        model="gpt-4",       
        temperature=0,
        max_tokens=512,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    for i, query in enumerate(QUERIES):
        print(f"\n[Baseline - Query {i+1}] {query}")

        prompt = f"Answer the following question:\n\n{query}"

        start_time = time.time()
        response = llm.predict(prompt)
        end_time = time.time()

        result_entry = {
            "query": query,
            "query_index": i + 1,
            "retrieved_fragments": 0,
            "dps_contributing": 0,
            "latency_ms": round((end_time - start_time) * 1000, 2),
            "redundancy_count": 0,
            "context_preview": None,
            "prompt_used": prompt[:500],
            "generated_answer": response
        }

        results_log.append(result_entry)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2)
    print(f"\n[Baseline] Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()