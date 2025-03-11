import torch
import torch.nn as nn
import torch.nn.functional as F
import dgl
from dgl.nn import HeteroGraphConv, GraphConv

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
def get_movie_recommendations(movie_id, movie_embeddings, top_k=5):
    """
    Given a movie ID, find the top-k most similar movies based on cosine similarity.
    """
    if movie_id >= len(movie_embeddings):
        print(f"Error: Movie ID {movie_id} is out of range.")
        return []
    
    movie_emb = movie_embeddings[movie_id]  # Get the embedding of the target movie
    movie_emb = movie_emb.unsqueeze(0)  # Reshape for similarity computation
    
    # Compute cosine similarity with all other movies
    similarity_scores = F.cosine_similarity(movie_emb, movie_embeddings)
    
    # Get top-k similar movies (excluding itself)
    top_k_indices = similarity_scores.argsort(descending=True)[1:top_k+1]  # Ignore self
    
    return top_k_indices, similarity_scores[top_k_indices]

# Step 6: Choose a movie ID and generate recommendations
movie_id = 20 # Change this to test different movies
top_k_movies, scores = get_movie_recommendations(movie_id, movie_embeddings, top_k=5)

# Step 7: Display the recommendations
print(f"\nTop 5 similar movies to Movie {movie_id}:")
for idx, score in zip(top_k_movies, scores):
    print(f"Movie {idx.item()} with similarity score: {score.item():.4f}")



import pandas as pd
# Load metadata
df = pd.read_csv("cleaned_movies.csv")
imdb_to_metadata = dict(zip(df["movie_id"], df["genre"]))  # Map IMDb ID to Genre
