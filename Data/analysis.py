import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('flattened_experiments_data.csv')

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

summary_c0 = summary[summary["n_people"] == 100]

# print(summary)

summary_c0.pivot(
    index="cohesion",
    columns="algorithm",
    values="mean_score"
).plot(
    title="Performance at with 100 people",
    xlabel="Cohesion",
    ylabel="Mean Score",
    marker="o"
)

plt.show()
# plt.savefig('performance_plot.png', dpi=300, bbox_inches='tight')
# print("Plot saved as 'performance_plot.png'")
# print(f"Plot shows performance comparison of {len(summary_c0['algorithm'].unique())} algorithms with 100 people across {len(summary_c0['cohesion'].unique())} cohesion levels")
