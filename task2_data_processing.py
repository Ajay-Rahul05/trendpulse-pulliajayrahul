import pandas as pd
import glob
import os
import sys


# ─────────────────────────────────────────────
# STEP 1 — Load the JSON file from data/ folder
# ─────────────────────────────────────────────

# Use glob to find the JSON file dynamically (filename has a date in it)
json_files = glob.glob("data/trends_*.json")

# If no file is found, exit early with a helpful message
if not json_files:
    print("ERROR: No trends JSON file found in the data/ folder.")
    sys.exit(1)

# Pick the first match (there should only be one)
json_path = json_files[0]

# Load the JSON into a DataFrame
# Pandas handles both list-of-objects and records-style JSON formats
df = pd.read_json(json_path)

# Show how many stories were loaded
print(f"Loaded {len(df)} stories from {json_path}")
print()


# ─────────────────────────────────────────────
# STEP 2 — Clean the Data
# ─────────────────────────────────────────────

# --- 2a. Remove duplicate rows based on post_id ---
# The same story might have been fetched twice across subreddits
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# --- 2b. Drop rows where critical fields are missing ---
# A story without a post_id, title, or score is not usable
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# --- 2c. Fix data types ---
# score and num_comments must be integers, not floats or strings
# errors="coerce" turns anything invalid into NaN so we can drop it safely
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce")

# Drop rows where conversion failed (i.e., score became NaN)
df = df.dropna(subset=["score"])

# Convert to proper integer type now that NaNs are gone
df["score"] = df["score"].astype(int)

# num_comments can have NaN (not all stories mention comments), fill with 0
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# --- 2d. Remove low-quality stories (score < 5) ---
# Stories with very low scores are likely spam or irrelevant
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")
print()

# --- 2e. Strip whitespace from the title column ---
# Titles sometimes have leading/trailing spaces from scraping
df["title"] = df["title"].str.strip()


# ─────────────────────────────────────────────
# STEP 3 — Save as CSV and print summary
# ─────────────────────────────────────────────

# Define output path
output_path = "data/trends_clean.csv"

# Ensure the data/ directory exists (in case it was deleted)
os.makedirs("data", exist_ok=True)

# Save cleaned DataFrame to CSV without the pandas index column
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
print()

# --- Print stories per category ---
# "category" column maps to subreddit (e.g., technology, sports)
print("Stories per category:")

# Value counts gives us frequency sorted by count (descending)
category_counts = df["category"].value_counts()

# Print each category with neat indentation for readability
for category, count in category_counts.items():
    print(f"  {category:<20} {count}")