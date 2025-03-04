# Assuming 'movie' nodes are stored in order in DGL
movie_imdb_ids = []  # List to store IMDb-style IDs in the order of DGL's node indices

import pandas as pd

# Load movie data from CSV
df = pd.read_csv("cleaned_movies.csv")  # Ensure it has a column 'movie_id'

# Extract IMDb IDs (ttXXXXX) in order
movie_imdb_ids = df["movie_id"].tolist()

# Create a mapping: DGL node index -> IMDb ID
node_index_to_imdb = {idx: imdb_id for idx, imdb_id in enumerate(movie_imdb_ids)}

# Save this mapping to a JSON file for later retrieval
import json
with open("node_index_to_imdb.json", "w") as f:
    json.dump(node_index_to_imdb, f)

print("DEBUG: Node-to-IMDb ID mapping saved.")