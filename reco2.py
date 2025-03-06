import torch
import torch.nn as nn
import torch.nn.functional as F
import dgl
from dgl.nn import HeteroGraphConv, GraphConv
import pandas as pd
import csv

# Step 1: Load the graph
graphs, _ = dgl.load_graphs("movie_graph.bin")
g = graphs[0]
print("DEBUG: Graph loaded successfully.")


# Step 2: Define the correct HeteroGNN model (same as used during training)
class HeteroGNN(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim, rel_names):
        super(HeteroGNN, self).__init__()
        self.conv1 = HeteroGraphConv({
            rel: GraphConv(in_dim, hidden_dim) for rel in rel_names
        }, aggregate='mean')
        self.conv2 = HeteroGraphConv({
            rel: GraphConv(hidden_dim, out_dim) for rel in rel_names
        }, aggregate='mean')

    def forward(self, g, inputs):
        h = self.conv1(g, inputs)
        h = {k: torch.relu(v) for k, v in h.items() if v is not None}  # Avoid None values
        h = self.conv2(g, h)
        return h  # Final node embeddings


# Step 3: Load the trained model with the correct architecture
in_dim = 128  # Ensure this matches your training setup
hidden_dim = 64
out_dim = 32
rel_names = g.etypes  # Extract relation names from the graph

# Create the model instance
model = HeteroGNN(in_dim, hidden_dim, out_dim, rel_names)

# Load the saved model state
model.load_state_dict(torch.load("hetero_gnn_model.pth"))
model.eval()  # Set model to evaluation mode
print("DEBUG: Model loaded successfully.")

# Step 4: Load the saved movie embeddings
movie_embeddings = torch.load("movie_embeddings.pth")
print("DEBUG: Movie embeddings loaded.")


# Step 5: Define a function for movie recommendations
def get_movie_recommendations(movie_ids, movie_embeddings, top_k=5):
    """
    Given a list of movie IDs, find the top-k most similar movies based on the average of their embeddings.
    """
    # Ensure all movie IDs are within bounds
    if any(movie_id >= len(movie_embeddings) for movie_id in movie_ids):
        print(f"Error: One or more movie IDs are out of range.")
        return []

    # Compute the average embedding for the given movie IDs
    movie_embs = movie_embeddings[movie_ids]  # Get the embeddings of the target movies
    avg_emb = movie_embs.mean(dim=0)  # Compute the average of the embeddings

    # Compute cosine similarity with all other movies
    similarity_scores = F.cosine_similarity(avg_emb.unsqueeze(0), movie_embeddings)

    # Exclude the input movie IDs from the top-k recommendations
    top_k_indices = similarity_scores.argsort(descending=True)  # Sort indices by similarity
    top_k_indices = [idx for idx in top_k_indices if idx.item() not in movie_ids]  # Exclude movie_ids from the recommendations
    top_k_indices = torch.tensor(top_k_indices)[:top_k]

    # Select similarity scores for the top-k movies
    top_k_scores = similarity_scores[top_k_indices]

    return top_k_indices, top_k_scores


# Step 6: Choose multiple movie IDs and generate recommendations
movie_ids = [968, 994]  # Example list of movie IDs to generate recommendations for
top_k_movies, scores = get_movie_recommendations(movie_ids, movie_embeddings, top_k=5)

import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return None


def get_name_by_id(csv_filepath, target_id):
    with open(csv_filepath, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        # Determine the index of 'ID' and 'Name' columns
        id_index = header.index('movie_id')
        name_index = header.index('movie_name')

        for row in reader:
            if row[id_index] == str(target_id):
                return row[name_index]
    return None

csv_filepath = 'cleaned_movies.csv'
file_path = 'node_index_to_imdb.json'
data = read_json_file(file_path)

# Step 7: Display the recommendations
print(f"\nTop 5 similar movies to Movies {movie_ids}:")
for movie_id in movie_ids:
    name = get_name_by_id(csv_filepath, data[str(movie_id)])
    print(f"({movie_id} = {name})")
# for idx, score in zip(top_k_movies, scores):
#     print(f"Movie {idx.item()} with similarity score: {score.item():.4f}")

# Step 8: Load metadata for genre information
df = pd.read_csv("cleaned_movies.csv")
imdb_to_metadata = dict(zip(df["movie_id"], df["genre"]))  # Map IMDb ID to Genre

# Example of displaying genre for the recommended movies
for idx, score in zip(top_k_movies, scores):
    genre = imdb_to_metadata.get(data[str(idx.item())], "Unknown")
    name = get_name_by_id(csv_filepath, data[str(idx.item())])
    print(f"({name}) Movie {idx.item()} with similarity score: {score.item():.4f}, Genre: {genre}")
