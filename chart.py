import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------
# 1) Synthetic, realistic data
# -------------------------
np.random.seed(42)

categories = [
    "Electronics",
    "Apparel",
    "Home & Kitchen",
    "Beauty & Health",
    "Sports & Outdoors",
]

# Average satisfaction (1–5) and realistic spread per category
means = {
    "Electronics": 4.1,
    "Apparel": 3.6,
    "Home & Kitchen": 4.3,
    "Beauty & Health": 4.0,
    "Sports & Outdoors": 3.8,
}
stds = {
    "Electronics": 0.45,
    "Apparel": 0.55,
    "Home & Kitchen": 0.35,
    "Beauty & Health": 0.40,
    "Sports & Outdoors": 0.50,
}

# Generate per‑customer scores (n ≈ 60 per category)
rows = []
for cat in categories:
    n = 60
    scores = np.random.normal(loc=means[cat], scale=stds[cat], size=n)
    scores = np.clip(scores, 1.0, 5.0)
    for s in scores:
        rows.append({"Category": cat, "Satisfaction": s})

df = pd.DataFrame(rows)

# -------------------------
# 2) Seaborn styling
# -------------------------
sns.set_style("whitegrid")
sns.set_context("talk")  # presentation-friendly text sizes

# -------------------------
# 3) Plot: mean with 95% CI
# -------------------------
plt.figure(figsize=(8, 8))  # 8in * 64 dpi = 512px
ax = sns.barplot(
    data=df,
    x="Category",
    y="Satisfaction",
    estimator=np.mean,
    errorbar=("ci", 95),          # Seaborn ≥0.12
    palette="deep",
    width=0.7,
    edgecolor="black",
)

# Titles and labels
ax.set_title("Customer Satisfaction by Product Category", pad=14, weight="bold")
ax.set_xlabel("Product Category")
ax.set_ylabel("Average Satisfaction (1–5)")

# Add value labels on bars (mean)
group_means = df.groupby("Category")["Satisfaction"].mean().reindex(categories)
for p, mean in zip(ax.patches, group_means):
    ax.annotate(f"{mean:.2f}", (p.get_x() + p.get_width()/2, p.get_height()),
                ha="center", va="bottom", fontsize=11, xytext=(0, 6), textcoords="offset points")

# Tidy ticks
ax.set_ylim(0, 5.2)
plt.xticks(rotation=15, ha="right")
plt.gcf().set_facecolor("white")

# -------------------------
# 4) Save exactly 512×512
# -------------------------
plt.savefig("chart.png", dpi=64, bbox_inches=None, pad_inches=0)   # 8in * 64dpi = 512px
plt.close()


print("Saved chart.png (512x512).")
