#  dsrag – Simulating RAG Architectures in Federated Data Spaces

This repository contains the experimental framework for evaluating six architectural models that integrate Retrieval-Augmented Generation (RAG) into federated Data Spaces (DSs).  
The goal is to analyze how different integration strategies affect trust-related properties such as **latency**, **relevance**, **traceability**, and **hallucination risk** in a modular, reproducible setup.

---

##  Project Structure

```
dsrag/
├── autonomous.py               # Centralized RAG: retrieval and generation by DC
├── source.py                   # Retrieval distributed at each DP
├── custodian.py                # Federator handles both retrieval and generation
├── guided.py                   # Federator retrieves; DC generates
├── federated.py                # Fully federated retrieval, with semantic structuring
├── baseline.py                 # No retrieval; LLM responds based on internal knowledge
├── core.py                     # Shared functions (load, index, retrieve)
├── queries.py                  # Shared set of six evaluation queries
├── generate_documents.py       # Generates realistic documents for three DPs
├── compare_responses.py        # Aggregates metrics and answers across models
├── generate_table.py           # Generates unified quantitative analysis tables
├── survey_analysis.py          # Processes qualitative survey responses
├── generate_review_template.py # Creates template for human evaluation
├── manual_review_template.csv  # CSV for qualitative assessment (generated)
├── data/                       # Document corpus per DP
├── indexes/                    # FAISS indexes by model
├── results_*.json              # Results per model (quantitative + generated answers)
├── comparison_table.csv        # Unified results table for quantitative analysis
├── qualitative_analysis/       # Final outputs of quantitative evaluation processing
├── survey_data/                # Raw survey responses for qualitative assessment
├── survey_analysis/            # Outputs of qualitative data processing
```

---

##  Motivation

**Data Spaces** are emerging infrastructures for sovereign, regulated data sharing.  
RAG architectures, when applied over such distributed ecosystems, require architectural decisions about **where retrieval occurs** and **how context is used**.

This framework evaluates:

-  Centralized vs. distributed retrieval  
-  Local vs. delegated generation  
-  Federated vs. guided aggregation  
-  Impact of retrieval vs. no retrieval (baseline)

---

##  Requirements

- Python **3.10+**
- Install dependencies:

```bash
pip install -r requirements.txt
```

- Create a `.env` file with your OpenAI API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

##  How to Use

### 1. Generate the Document Corpus

```bash
python generate_documents.py
```

This creates realistic domain-specific texts for three Data Providers:
- A hospital research institute  
- A European data protection authority  
- A bioethics-focused NGO

---

### 2. Run All Architectural Simulations

```bash
python autonomous.py
python source.py
python custodian.py
python guided.py
python federated.py
python baseline.py
```

Each script saves a `results_*.json` file with the model’s output and evaluation metrics.

---

### 3. Compare Results Automatically

```bash
python compare_responses.py
```

This aggregates metrics and generated answers into `comparison_table.csv` and prints responses grouped by query and model.

---

### 4. Generate a Human Evaluation Template

```bash
python generate_review_template.py
```

Creates `manual_review_template.csv` for scoring based on:

- Relevance  
- Hallucination risk  
- Traceability  
- Semantic consistency  

---

### 5. Generate Quantitative Analysis Tables

```bash
python generate_table.py
```

Processes all `results_*.json` files and generates consolidated tables under `qualitative_analysis/`.

---

### 6. Process Qualitative Survey Results

```bash
python survey_analysis.py
```

Processes raw survey responses stored in `survey_data/` and generates outputs in `survey_analysis/`.

**Includes:**
- Aggregated Likert-scale scores for all qualitative criteria  
- Calculation of **Krippendorff’s Alpha** for inter-rater agreement

> ℹ️ *Krippendorff’s Alpha* accounts for chance agreement, handles missing data, and supports ordinal metrics—ideal for rigorous annotation analysis.

---

##  Evaluation Design

- All models use the same **six queries** (five domain-specific + one control).
- **Latency** is measured per query (excluding index build time).
- In `federated.py`, retrieval is **sequential** to simulate worst-case delays.
- Retrieved context is grouped and **source-tagged** for semantic structure.

---

##  Metrics Collected

| Metric                | Description                                          |
|-----------------------|------------------------------------------------------|
| `latency_ms`          | Time from query start to retrieval end               |
| `retrieved_fragments` | Number of fragments retrieved                        |
| `dps_contributing`    | Number of DPs contributing relevant content          |
| `redundancy_count`    | Number of duplicate fragments in final context       |
| `generated_answer`    | Raw output from the language model                   |

All outputs are stored as structured `.json` files.

---

##  Qualitative Evaluation

Reviewers manually score each answer using Likert scales (1–5) for:

-  Relevance  
-  Hallucination Risk  
-  Traceability  
-  Semantic Consistency  

Manual scoring templates support reproducibility and inter-rater analysis.

---

##  Citation

This framework supports an academic study on trust-aware RAG integration in federated systems.  
If you use or extend it, please **cite the associated paper** or **contact the authors**.

---

##  Contact

For questions, collaborations or academic inquiries:

**Carlos Mario Braga**  
 carlosmario.braga1@alu.uclm.es
