# Global Power Plant Database — NumPy, Pandas & Matplotlib Integration

Analysis of the [Global Power Plant Database](https://datasets.wri.org/dataset/globalpowerplantdatabase) (~35,000 plants worldwide) using Python's core data science stack.

## Key Insights

- **Nuclear plants** are the largest by average capacity (~1,800 MW), while **Solar** and **Wind** installations are numerous but individually smaller.
- **Statistical testing** (Kruskal-Wallis, Mann-Whitney U) confirms significant capacity differences between fuel types.
- **Renewable capacity additions** (Solar + Wind) have been accelerating since ~2005, with a clear exponential trend visible in the data.
- The **2010s** represent a turning point: Solar and Wind went from marginal to dominant in new capacity additions. Coal new builds peaked in the 2000s.
- **PCA/Eigenvalue decomposition** on the correlation matrix shows that capacity and generation are strongly correlated (same underlying dimension), while geographic coordinates add independent information.

## Tasks Covered

| # | Task | Description |
|---|------|-------------|
| 1 | Data Import & Cleaning | Missing value handling, type conversion, generation consolidation |
| 2 | Exploratory Data Analysis | Summary stats, country/fuel distributions |
| 3 | Statistical Analysis | Kruskal-Wallis + pairwise Mann-Whitney tests on capacity by fuel |
| 4 | Time Series Analysis | Commissioning trends, fuel mix evolution, linear trend fitting |
| 5 | Advanced Visualization | Geographic scatter, heatmaps, violin plots |
| 6 | Matrix Operations | Correlation eigendecomposition, PCA interpretation |
| 7 | NumPy Integration | Complex filtering, rolling stats, matrix multiplication scoring |

## How to Run

```bash
pip install numpy pandas matplotlib seaborn scipy jupyter
jupyter notebook global_power_plant_analysis.ipynb
```

Place `global_power_plant_database.csv` in the same directory as the notebook.

## Tech Stack

- **NumPy** — statistical functions, polyfit, eigendecomposition, convolution, boolean masks
- **Pandas** — data loading, groupby, pivot tables, filtering
- **Matplotlib + Seaborn** — bar charts, heatmaps, scatter, violin plots, fitted curves
- **SciPy** — hypothesis testing (Kruskal-Wallis, Mann-Whitney U)
