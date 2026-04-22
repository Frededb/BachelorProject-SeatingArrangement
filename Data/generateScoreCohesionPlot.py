import pandas as pd
import matplotlib.pyplot as plt

people = 300
algorithm_colors = {
    "annealingFromFluent": "tab:blue",
    "annealingFromRandom": "tab:orange",
    "bruteForce": "tab:green",
    "linearSwitchFromFluent": "tab:red",
    "linearSwitchFromFluentProtected": "tab:purple",
    "linearSwitchFromRandom": "tab:brown",
    "randomSwitchFromFluent": "tab:pink",
    "randomSwitchFromRandom": "tab:gray",
    "tabuSearchFromFluent": "tab:olive",
    "tabuSearchFromRandom": "tab:cyan",
}

df = pd.read_csv('flattened_composite_experiments_data.csv')

# Convert score and time to numeric types, coercing invalid values to NaN
df['score'] = pd.to_numeric(df['score'], errors='coerce')
df['time'] = pd.to_numeric(df['time'], errors='coerce')

# Remove rows with NaN values
df = df.dropna()

# print(df)

summary = df.groupby(["algorithm", "n_people", "cohesion"]).agg(
    mean_score=("score", "mean"),
    std_score=("score", "std"),
    mean_time=("time", "mean"),
    std_time=("time", "std"),
).reset_index()

summary_c0 = summary[summary["n_people"] == people]

# print(summary)

pivot_data = summary_c0.pivot(
    index="cohesion",
    columns="algorithm",
    values="mean_score"
)

# Filter colors to only include algorithms in the pivot table
colors = {algo: algorithm_colors.get(algo, "tab:gray") for algo in pivot_data.columns}

pivot_data.plot(
    title=f"Performance at with {people} people",
    xlabel="Cohesion",
    ylabel="Mean Score",
    marker="o",
    color=colors
)
plt.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=2
)
plt.tight_layout(rect=[0, 0.01, 1, 1])
plt.savefig(f'plots/{people}p_score_cohesion_plot.png', dpi=300, bbox_inches='tight')
plt.show()

# print("Plot saved as 'performance_plot.png'")
# print(f"Plot shows performance comparison of {len(summary_c0['algorithm'].unique())} algorithms with 100 people across {len(summary_c0['cohesion'].unique())} cohesion levels")
