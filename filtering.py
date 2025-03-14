import pandas as pd
import numpy as np
import os
import glob

data_directory = "movie_data"
# movie_data directory 
file_paths = glob.glob(os.path.join(data_directory, "*.csv"))

df_list = [pd.read_csv(file) for file in file_paths]
df = pd.concat(df_list, ignore_index=True)

# Select only the relevant columns
columns_to_keep = ["movie_name", "movie_id", "year", "genre", "rating", "director_id", "star_id", "votes", "description"]
df = df[columns_to_keep]

# Track initial number of entries
initial_entries = df.shape[0]

# Convert data types
df["year"] = pd.to_numeric(df["year"], errors='coerce')
df["rating"] = pd.to_numeric(df["rating"], errors='coerce')
df["votes"] = pd.to_numeric(df["votes"], errors='coerce')

# Handle missing values
df["rating"].fillna(df["rating"].median(), inplace=True)
df["votes"].fillna(df["votes"].median(), inplace=True)
df["director_id"].fillna("unknown_director", inplace=True)
df["star_id"].fillna("unknown_star", inplace=True)
df["description"].fillna("no description provided", inplace=True)

# Remove low-quality movies (e.g., low votes and ratings)
df_filtered = df[(df["votes"] >= 100000) & (df["rating"] >= 4.5)]

# shows how many entries is dropped 
filtered_out_entries = df.shape[0] - df_filtered.shape[0]

# drop out duplicates 
df_unique = df_filtered.drop_duplicates(subset=["movie_id"])

duplicates_removed = df_filtered.shape[0] - df_unique.shape[0]

# Normalize rating and votes
df_unique["normalized_rating"] = (df_unique["rating"] - df_unique["rating"].min()) / (df_unique["rating"].max() - df_unique["rating"].min())
df_unique["normalized_votes"] = (df_unique["votes"] - df_unique["votes"].min()) / (df_unique["votes"].max() - df_unique["votes"].min())

# Convert genre column into list format
df_unique["genre"] = df_unique["genre"].str.split(",")

# Save cleaned data
df_unique.to_csv("cleaned_movies.csv", index=False)

# Print statistics
final_entries = df_unique.shape[0]

print(f"Initial entries: {initial_entries}")
print(f"Entries removed due to filtering (low votes/rating): {filtered_out_entries}")
print(f"Duplicate movies removed: {duplicates_removed}")
print(f"Final cleaned dataset size: {final_entries}")