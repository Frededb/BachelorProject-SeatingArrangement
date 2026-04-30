import json
import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("plots", exist_ok=True)

with open("../Inputs/realData/inputReal.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# Optional: nicer labels
df["studyprogram"] = df["studyprogram"].str.upper()
df["year"] = df["year"].astype(str)

def make_pie(series, title, filename, legend_title=None):
    counts = series.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        counts,
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
        pctdistance=0.8,
        textprops={'fontsize': 10}
    )

    ax.set_title(title)
    ax.axis("equal")  # makes it circular

    if legend_title:
        ax.legend(
            wedges,
            counts.index,
            title=legend_title,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.1)
        )

    fig.savefig(filename, dpi=300, bbox_inches="tight")
    plt.show()

make_pie(
    df["year"],
    "Distribution of Years",
    "plots/year_distribution_pie.png",
    legend_title="Year"
)

make_pie(
    df["studyprogram"],
    "Distribution of Study Programs",
    "plots/studyprogram_distribution_pie.png",
    legend_title="Study Program"
)