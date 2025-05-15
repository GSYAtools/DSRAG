import os
import json
import pandas as pd

# Ruta
folder_path = './'

filename_to_rag = {
    "results_federated.json": "Federated",
    "results_guided.json": "Guided",
    "results_custodian.json": "Custodian",
    "results_baseline.json": "Baseline",
    "results_autonomous.json": "Autonomous",
    "results_at_source.json": "Source"
}

rows = []

for filename, rag_label in filename_to_rag.items():
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r') as f:
        data = json.load(f)

    for entry in data:
        row = {
            "RAG": rag_label,
            "Query Index": entry.get("query_index"),
            "Retrieved Fragments": entry.get("retrieved_fragments"),
            "DPs Contributing": entry.get("dps_contributing"),
            "Latency (ms)": entry.get("latency_ms"),
            "Redundancy": entry.get("redundancy_count")
        }
        rows.append(row)

df = pd.DataFrame(rows)

# Agrupación
agg = df.groupby("RAG").agg(["mean", "std"]).round(2)
agg.columns = [' '.join(col).strip() for col in agg.columns]
agg.reset_index(inplace=True)

# Orden deseado
model_order = ["Autonomous", "Source", "Custodian", "Guided", "Federated", "Baseline"]
agg.set_index("RAG", inplace=True)
agg = agg.loc[model_order].reset_index()

# Generación de tabla LaTeX
latex = r"""
\begin{table}[htbp]
\centering
\caption{Quantitative evaluation of the six architectures. Values are averaged over six test queries and include standard deviation ($\sigma$).}
\label{tab:quantitative-results}
\begin{tabular}{|l|cc|cc|cc|cc|}
\hline
\textbf{Model} & \multicolumn{2}{c|}{\textbf{Latency (ms)}} & \multicolumn{2}{c|}{\textbf{Fragments Retrieved}} & \multicolumn{2}{c|}{\textbf{DPs Contributing}} & \multicolumn{2}{c|}{\textbf{Redundancy}} \\
              & Mean & $\sigma$ & Mean & $\sigma$ & Mean & $\sigma$ & Mean & $\sigma$ \\
\hline
"""

for _, row in agg.iterrows():
    latex += f"{row['RAG']:12} & {row['Latency (ms) mean']:.2f} & {row['Latency (ms) std']:.2f} & "
    latex += f"{row['Retrieved Fragments mean']:.2f} & {row['Retrieved Fragments std']:.2f} & "
    latex += f"{row['DPs Contributing mean']:.2f} & {row['DPs Contributing std']:.2f} & "
    latex += f"{row['Redundancy mean']:.2f} & {row['Redundancy std']:.2f} \\\\\n"

latex += r"""\hline
\end{tabular}
\end{table}
"""

print(latex)