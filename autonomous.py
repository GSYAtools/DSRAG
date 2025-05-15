import os
import time
import json
from core import load_documents, create_faiss_index, query_index
from queries import QUERIES

# Configuración
DPS = ["data/dp1", "data/dp2", "data/dp3"]
INDEX_DIR = "indexes/autonomous"
RESULTS_FILE = "results_autonomous.json"

def main():
    os.makedirs(INDEX_DIR, exist_ok=True)

    print("[Autonomous] Loading documents from all DPs...")
    docs = load_documents(DPS)

    print("[Autonomous] Creating unified index...")
    create_faiss_index(docs, INDEX_DIR)

    results_log = []

    for i, query in enumerate(QUERIES):
        print(f"\n[Query {i+1}] {query}")
        start_time = time.time()
        results = query_index(INDEX_DIR, query)
        end_time = time.time()

        context = [doc.page_content for doc in results]
        dps_used = list(set(doc.metadata["dp"] for doc in results))
        redundancy = len(context) - len(set(context))  # simple redundancy metric

        # --- RAG PROMPT (context + query) ---
        retrieved_context = "\n\n".join(context)
        prompt = (
            f"Answer the following question based only on the context below.\n\n"
            f"Context:\n{retrieved_context}\n\n"
            f"Question: {query}"
        )

        # --- GENERATE RESPONSE 
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        response = llm.predict(prompt)

        # --- Save result ---
        result_entry = {
            "query": query,
            "query_index": i + 1,
            "retrieved_fragments": len(results),
            "dps_contributing": len(dps_used),
            "latency_ms": round((end_time - start_time) * 1000, 2),
            "redundancy_count": redundancy,
            "context_preview": [c[:200] for c in context],
            "prompt_used": prompt[:500],
            "generated_answer": response
        }

        results_log.append(result_entry)

    # Guardar resultados
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2)
    print(f"\n[Autonomous] Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
