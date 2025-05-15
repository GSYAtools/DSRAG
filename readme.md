# dsrag – Simulating RAG Architectures in Federated Data Spaces

This repository contains the experimental framework for evaluating six architectural models that integrate Retrieval-Augmented Generation (RAG) into federated Data Spaces (DSs). The goal is to analyze how different integration strategies affect trust-related properties such as latency, relevance, traceability, and hallucination risk in a modular, reproducible setup.

---

## Project Structure

dsrag/

├── autonomous.py              # Centralized RAG: retrieval and generation by DC

├── source.py                  # Retrieval distributed at each DP

├── custodian.py               # Federator handles both retrieval and generation

├── guided.py                  # Federator retrieves; DC generates
├── federated.py               # Fully federated retrieval, with semantic structuring
├── baseline.py                # No retrieval; LLM responds based on internal knowledge
├── core.py                    # Shared functions (load, index, retrieve)
├── queries.py                 # Shared set of six evaluation queries
├── generate_documents.py      # Generates realistic documents for three DPs
├── compare_responses.py       # Aggregates metrics and answers across models
├── generate_review_template.py# Creates template for human evaluation
├── manual_review_template.csv # CSV for qualitative assessment (generated)
├── data/                      # Document corpus per DP
├── indexes/                   # FAISS indexes by model
├── results_*.json             # Results per model (quantitative + generated answers)
└── comparison_table.csv       # Unified results table for analysis

---

## Motivation

Data Spaces are emerging infrastructures for sovereign, regulated data sharing. RAG architectures, when applied over such distributed ecosystems, require architectural decisions about where retrieval occurs and how context is used.

This framework evaluates:
- Centralized vs. distributed retrieval
- Local vs. delegated generation
- Federated vs. guided aggregation
- Impact of retrieval vs. no retrieval (baseline)

---

## Requirements

- Python 3.10+
- Install dependencies:

pip install -r requirements.txt

- Create a `.env` file with your OpenAI API key:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

---

## How to Run the Experiments

1. Generate the document corpus

python generate_documents.py

This creates realistic domain-specific texts for three Data Providers:
- A hospital research institute
- A European data protection authority
- A bioethics-focused NGO

2. Run all architectural simulations

python autonomous.py
python source.py
python custodian.py
python guided.py
python federated.py
python baseline.py

This executes six architectures and saves one `results_*.json` file per model.

3. Compare results automatically

python compare_responses.py

This aggregates metrics and answers into `comparison_table.csv` and prints all responses by query and model.

4. Generate a human evaluation template

python generate_review_template.py

Creates `manual_review_template.csv` for scoring responses on:
- Relevance
- Hallucination risk
- Traceability
- Semantic consistency

---

## Evaluation Design

- All models use the same six queries (five domain-specific + one control).
- Latency is measured per query (excluding index time).
- Federated retrieval is performed **sequentially** to simulate worst-case latency.
- In `federated.py`, context is grouped and tagged by source (e.g., `[Context from DP1]`) to enable semantically structured prompts.

---

## Metrics Collected

| Metric              | Description                                      |
|---------------------|--------------------------------------------------|
| `latency_ms`        | From query start to retrieval end                |
| `retrieved_fragments` | Number of fragments retrieved                 |
| `dps_contributing`  | Number of DPs returning relevant content         |
| `redundancy_count`  | Duplicate fragments in context                   |
| `generated_answer`  | Raw output from the LLM                          |

All results are stored as structured `.json` files.

---

## Qualitative Evaluation

Human reviewers score responses using a CSV template and 1–5 Likert scales for:
- Answer relevance
- Hallucination risk
- Traceability and attribution
- Semantic consistency across sources

Manual scoring supports replication and inter-annotator evaluation.

---

## Citation

This framework supports an academic study on trust-aware RAG integration in federated systems. If you use or extend it, please cite the associated paper or contact the authors.

---

## Contact

For questions or collaboration:

**Carlos Mario Braga**  
carlosmario.braga1@alu.uclm.es
