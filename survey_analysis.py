import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from statsmodels.stats.inter_rater import fleiss_kappa
from sklearn.preprocessing import OneHotEncoder
import os

# Rutas fijas
INPUT_PATH = "survey_data/mi_encuesta.csv"
OUTPUT_DIR = "survey_analysis"

def cargar_datos(path_csv):
    df = pd.read_csv(path_csv)
    df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
    return df

def calcular_estadisticas_modelo_dimension(df):
    grouped = df.groupby(['Model', 'Dimension'])['Score'].agg([
        'mean', 'std', lambda x: Counter(x).most_common(1)[0][0]
    ]).reset_index()
    grouped.columns = ['Model', 'Dimension', 'Mean', 'StdDev', 'Mode']
    return grouped

def calcular_estadisticas_modelo_agregado(df):
    # Excluir 'Hallucination Risk' antes de agrupar
    df_filtrado = df[df['Dimension'] != 'Hallucination Risk']
    
    grouped = df_filtrado.groupby('Model')['Score'].agg([
        'mean', 'std', lambda x: Counter(x).most_common(1)[0][0]
    ]).reset_index()
    grouped.columns = ['Model', 'Mean', 'StdDev', 'Mode']
    return grouped

def graficar_estadisticas_por_dimension(df_stats, output_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    modelos = df_stats['Model'].unique()
    dimensiones = df_stats['Dimension'].unique()

    x = np.arange(len(dimensiones))
    width = 0.12  # anchura de barras mejorada para legibilidad

    fig, ax = plt.subplots(figsize=(14, 6))  # figura más ancha

    for i, model in enumerate(modelos):
        subset = df_stats[df_stats['Model'] == model]
        subset = subset.set_index('Dimension').reindex(dimensiones).reset_index()
        means = subset['Mean'].values
        stds = subset['StdDev'].values

        ax.bar(
            x + i * width,
            means,
            width,
            yerr=stds,
            label=model,
            capsize=3
        )

    ax.set_xticks(x + width * (len(modelos) - 1) / 2)
    ax.set_xticklabels(dimensiones, rotation=45, fontsize=11)
    ax.set_ylabel("Average Score", fontsize=12)
    ax.legend(fontsize=10, ncol=2, loc="upper left", bbox_to_anchor=(1, 1))

    plt.tight_layout()
    output_path = os.path.join(output_dir, "media_por_dimension.png")
    plt.savefig(output_path)
    plt.close()

    
def graficar_estadisticas_agregadas(df_stats, output_dir):
    import matplotlib.pyplot as plt
    import numpy as np
    import os

    fig, ax = plt.subplots(figsize=(10, 5))  # figura más ancha

    x = np.arange(len(df_stats))
    means = df_stats['Mean'].values
    stds = df_stats['StdDev'].values
    labels = df_stats['Model'].values

    ax.bar(x, means, yerr=stds, capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, fontsize=11)
    ax.set_ylabel("Average Score", fontsize=12)
    ax.grid(axis="y", linestyle="--", linewidth=0.5, alpha=0.6)

    plt.tight_layout()
    output_path = os.path.join(output_dir, "media_por_modelo.png")
    plt.savefig(output_path)
    plt.close()

def calcular_krippendorff_alpha(df):
    pivot = df.pivot_table(index=['Query', 'Dimension'], columns='Evaluator', values='Score')
    encoded = []

    for row in pivot.values:
        if np.all(np.isnan(row)):
            continue
        counter = Counter(row[~np.isnan(row)].astype(int))
        encoded.append([counter.get(i, 0) for i in range(1, 6)])

    encoded_array = np.array(encoded)

    if encoded_array.shape[0] < 2:
        return None

    return fleiss_kappa(encoded_array)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = cargar_datos(INPUT_PATH)

    # Estadísticas por modelo y dimensión
    stats_model_dim = calcular_estadisticas_modelo_dimension(df)
    stats_model_dim.to_csv(os.path.join(OUTPUT_DIR, "estadisticas_modelo_dimension.csv"), index=False)

    # Estadísticas globales por modelo
    stats_model = calcular_estadisticas_modelo_agregado(df)
    stats_model.to_csv(os.path.join(OUTPUT_DIR, "estadisticas_modelo_global.csv"), index=False)

    # Gráficos
    graficar_estadisticas_por_dimension(stats_model_dim, OUTPUT_DIR)
    graficar_estadisticas_agregadas(stats_model, OUTPUT_DIR)

    # Krippendorff’s Alpha
    alpha = calcular_krippendorff_alpha(df)
    with open(os.path.join(OUTPUT_DIR, "krippendorff_alpha.txt"), "w") as f:
        if alpha is not None:
            f.write(f"Krippendorff’s Alpha: {alpha:.3f}\n")
        else:
            f.write("No hay suficientes evaluaciones coincidentes para calcular Krippendorff’s Alpha.\n")

    print(f" Análisis completado. Resultados guardados en: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
