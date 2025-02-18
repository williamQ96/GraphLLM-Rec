import pandas as pd
import numpy as np

# Load all 16 CSV files into a single dataframe
file_paths = ["file1.csv", "file2.csv", ..., "file16.csv"]  # Update with actual file names
df_list = [pd.read_csv(file) for file in file_paths]
df = pd.concat(df_list, ignore_index=True)

# Select only the relevant columns
columns_to_keep = ["movie_id", "year", "runtime", "genre", "rating", "director_id", "star_id", "votes", "gross(in $)"]
df = df[columns_to_keep]

# Convert data types
df["year"] = pd.to_numeric(df["year"], errors='coerce')
df["runtime"] = pd.to_numeric(df["runtime"], errors='coerce')
df["rating"] = pd.to_numeric(df["rating"], errors='coerce')
df["votes"] = pd.to_numeric(df["votes"], errors='coerce')
df["gross(in $)"] = pd.to_numeric(df["gross(in $)"], errors='coerce')

# Handle missing values
df["rating"].fillna(df["rating"].median(), inplace=True)
df["runtime"].fillna(df["runtime"].median(), inplace=True)
df["votes"].fillna(df["votes"].median(), inplace=True)
df["gross(in $)"].fillna(df["gross(in $)"].median(), inplace=True)
df["director_id"].fillna("unknown_director", inplace=True)
df["star_id"].fillna("unknown_star", inplace=True)

# Remove low-quality movies (e.g., low votes and ratings)
df = df[(df["votes"] >= 1000) & (df["rating"] >= 4.0)]

# Normalize rating and votes
df["normalized_rating"] = (df["rating"] - df["rating"].min()) / (df["rating"].max() - df["rating"].min())
df["normalized_votes"] = (df["votes"] - df["votes"].min()) / (df["votes"].max() - df["votes"].min())

# Convert genre column into list format
df["genre"] = df["genre"].str.split(",")

# Save cleaned data
df.to_csv("cleaned_movies.csv", index=False)

print("Data Cleaning Complete. Final shape:", df.shape)
