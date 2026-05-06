import json
import pandas as pd
import matplotlib.pyplot as plt

FILE = "comparison_results_randomSwitchFromRandom.json"

with open(FILE, encoding="utf-8") as f:
    data = json.load(f)

algo_results = next(iter(data["results"].values()))
people_count = next(iter(algo_results.keys()))
cohesion_data = algo_results[people_count]

fig, ax = plt.subplots(figsize=(12, 7))

for cohesion, entry in sorted(cohesion_data.items(), key=lambda x: int(x[0])):
    # Use first iteration's timeline
    timeline = entry["timelines"][0]
    df = pd.DataFrame(timeline, columns=["time", "score"])
    ax.plot(df["time"], df["score"], label=f"cohesion={cohesion}")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Score")
ax.set_title(f"Timeline scores by cohesion ({FILE})")
ax.legend(loc="lower right")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("timeline_plot.png", dpi=150)
plt.show()
print("Saved to timeline_plot.png")
