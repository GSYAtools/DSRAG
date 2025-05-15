import os
import time
import json
from core import load_documents, create_faiss_index, query_index
from queries import QUERIES

DPS = ["data/dp1", "data/dp2", "data/dp3"]
INDEX_BASE = "indexes/federated"
RESULTS_FILE = "results_federated.json"

def main():
    os.makedirs(INDEX_BASE, exist_ok=True)

    # Crear índice local en cada DP
    for dp_path in DPS:
        dp_name = os.path.basename(dp_path)
        index_path = os.path.join(INDEX_BASE, dp_name)
        os.makedirs(index_path, exist_ok=True)
        docs = load_documents([dp_path])
        create_faiss_index(docs, index_path)

    results_log = []

    for i, query in enumerate(QUERIES):
        print(f"\n[Query {i+1}] {query}")
        start_time = time.time()

        all_results = []
        for dp_path in DPS:
            dp_name = os.path.basename(dp_path)
            index_path = os.path.join(INDEX_BASE, dp_name)
            dp_results = query_index(index_path, query)
            all_results.extend(dp_results)

        end_time = time.time()

        context = [doc.page_content for doc in all_results]
        dps_used = list(set(doc.metadata["dp"] for doc in all_results))
        redundancy = len(context) - len(set(context))

        retrieved_context = "\n\n".join(
            f"[{doc.metadata['dp']}] {doc.page_content}" for doc in all_results
        )

        prompt = (
            f"Answer the following question based only on the context below.\n\n"
            f"Context:\n{retrieved_context}\n\n"
            f"Question: {query}"
        )

        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4", temperature=0)
        response = llm.predict(prompt)
        
        result_entry = {
            "query": query,
            "query_index": i + 1,
            "retrieved_fragments": len(all_results),
            "dps_contributing": len(dps_used),
            "latency_ms": round((end_time - start_time) * 1000, 2),
            "redundancy_count": redundancy,
            "context_preview": [c[:200] for c in context],
            "prompt_used": prompt[:500],
            "generated_answer": response
        }

        results_log.append(result_entry)

    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(results_log, f, indent=2)
    print(f"\n[Federated] Results saved to {RESULTS_FILE}")

if __name__ == "__main__":
    main()
