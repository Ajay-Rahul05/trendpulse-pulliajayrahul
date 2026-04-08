import os
import pandas as pd
import matplotlib.pyplot as plt

# Create outputs folder if it does not exist
os.makedirs("outputs", exist_ok=True)

# Load the CSV file
df = pd.read_csv("data/trends_analysed.csv")

# -----------------------------
# Chart 1: Top 10 Stories by Score
# -----------------------------

# Get top 10 stories by score
top_stories = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
short_titles = [
    title[:50] + "..." if len(title) > 50 else title
    for title in top_stories["title"]
]

plt.figure(figsize=(12, 8))
plt.barh(short_titles, top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # Highest score at the top
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()

# -----------------------------
# Chart 2: Stories per Category
# -----------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(10, 6))
plt.bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10.colors[:len(category_counts)]
)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()

# -----------------------------
# Chart 3: Score vs Comments
# -----------------------------

popular_stories = df[df["is_popular"] == True]
non_popular_stories = df[df["is_popular"] == False]

plt.figure(figsize=(10, 6))

plt.scatter(
    popular_stories["score"],
    popular_stories["num_comments"],
    label="Popular",
    alpha=0.7
)

plt.scatter(
    non_popular_stories["score"],
    non_popular_stories["num_comments"],
    label="Not Popular",
    alpha=0.7
)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()

# -----------------------------
# Bonus: Combined Dashboard
# -----------------------------

fig, axes = plt.subplots(1, 3, figsize=(22, 7))

# Dashboard Chart 1
axes[0].barh(short_titles, top_stories["score"])
axes[0].set_title("Top 10 Stories by Score")
axes[0].set_xlabel("Score")
axes[0].set_ylabel("Story Title")
axes[0].invert_yaxis()

# Dashboard Chart 2
axes[1].bar(
    category_counts.index,
    category_counts.values,
    color=plt.cm.tab10.colors[:len(category_counts)]
)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")
axes[1].set_ylabel("Number of Stories")
axes[1].tick_params(axis="x", rotation=45)

# Dashboard Chart 3
axes[2].scatter(
    popular_stories["score"],
    popular_stories["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[2].scatter(
    non_popular_stories["score"],
    non_popular_stories["num_comments"],
    label="Not Popular",
    alpha=0.7
)

axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Number of Comments")
axes[2].legend()

fig.suptitle("TrendPulse Dashboard", fontsize=16)
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()