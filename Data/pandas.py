import pandas as pd

df = pd.read_csv('../Data/flattened_experiments_data.csv')

# print(df)

summary = df.groupby(["algorithm", "people_count", "cohesion_score"]).agg(
    mean_score=("score", "mean"),
    std_score=("score", "std"),
    mean_time=("time", "mean"),
    std_time=("time", "std"),
).reset_index()

print(summary)