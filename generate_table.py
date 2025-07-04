import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Rutas
folder_path = './'
output_path = './cuantitative_analysis/'
os.makedirs(output_path, exist_ok=True)

# Archivos de entrada
filename_to_rag = {
    "results_federated.json": "Federated",
    "results_guided.json": "Guided",
    "results_custodian.json": "Custodian",
    "results_baseline.json": "Baseline",
    "results_autonomous.json": "Autonomous",
    "results_at_source.json": "Source"
}

# Leer JSONs y construir dataframe
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

# Agrupar y calcular estadísticas
agg = df.groupby("RAG").agg(["mean", "std"]).round(2)
agg.columns = [' '.join(col).strip() for col in agg.columns]
agg.reset_index(inplace=True)

# Ordenar modelos como en análisis cualitativo
model_order = ["Autonomous", "Source", "Custodian", "Guided", "Federated", "Baseline"]
agg.set_index("RAG", inplace=True)
agg = agg.loc[model_order].reset_index()

# 1. Exportar CSV
csv_path = os.path.join(output_path, "estadisticas_modelo_cuantitativas.csv")
agg.to_csv(csv_path, index=False)

# 2. Generar tabla LaTeX
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
    latex += f"{row['RAG']:12} & "
    latex += f"${row['Latency (ms) mean']:.2f} \\pm {row['Latency (ms) std']:.2f}$ & "
    latex += f"${row['Retrieved Fragments mean']:.2f} \\pm {row['Retrieved Fragments std']:.2f}$ & "
    latex += f"${row['DPs Contributing mean']:.2f} \\pm {row['DPs Contributing std']:.2f}$ & "
    latex += f"${row['Redundancy mean']:.2f} \\pm {row['Redundancy std']:.2f}$ \\\\\n"

latex += r"""\hline
\end{tabular}
\end{table}
"""

with open(os.path.join(output_path, "tabla_quant_eval.tex"), "w", encoding="utf-8") as f:
    f.write(latex)

# 3. Preparar DataFrame largo para graficar
metrics = ["Latency (ms)", "Retrieved Fragments", "DPs Contributing", "Redundancy"]
plot_data = []

for metric in metrics:
    for _, row in agg.iterrows():
        plot_data.append({
            "Model": row["RAG"],
            "Metric": metric,
            "Mean": row[f"{metric} mean"],
            "Std": row[f"{metric} std"]
        })

df_plot = pd.DataFrame(plot_data)

# 4. Gráfico con doble eje: Latency a la izquierda, resto a la derecha
plt.figure(figsize=(14, 6))
fig, ax = plt.subplots(figsize=(14, 6))

x = np.arange(len(model_order))
width = 0.2

# Eje izquierdo: Latency (ms)
lat_means = []
lat_stds = []
for model in model_order:
    row = df_plot[(df_plot["Model"] == model) & (df_plot["Metric"] == "Latency (ms)")].iloc[0]
    lat_means.append(row["Mean"])
    lat_stds.append(row["Std"])

ax.bar(x - width, lat_means, width, yerr=lat_stds, capsize=4, label="Latency (ms)", color='tab:blue')
ax.set_ylabel("Latency (ms)", color='tab:blue')
ax.tick_params(axis='y', labelcolor='tab:blue')

# Eje derecho: otras métricas
ax2 = ax.twinx()
metrics_right = ["Retrieved Fragments", "DPs Contributing", "Redundancy"]
colors = ['tab:green', 'tab:orange', 'tab:red']

for i, metric in enumerate(metrics_right):
    means = []
    stds = []
    for model in model_order:
        row = df_plot[(df_plot["Model"] == model) & (df_plot["Metric"] == metric)].iloc[0]
        means.append(row["Mean"])
        stds.append(row["Std"])
    offset = width * (i + 1)
    ax2.bar(x + offset, means, width, yerr=stds, capsize=4, label=metric, color=colors[i])

ax2.set_ylabel("Fragments / DPs / Redundancy", color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Eje X
ax.set_xticks(x)
ax.set_xticklabels(model_order, rotation=30)

# Título y leyenda
plt.title("Quantitative Metrics by Model")
fig.legend(loc='upper left', bbox_to_anchor=(0.13, 0.95), ncol=2)

plt.tight_layout()
plt.savefig(os.path.join(output_path, "media_cuantitativa_dual_axis.png"))
plt.close()