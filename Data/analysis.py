import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../Data/flattened_experiments_data.csv')

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