import dgl
import torch
import torch.nn as nn
from dgl.nn import HeteroGraphConv, GraphConv
import torch.optim as optim
import torch.nn.functional as F

# Load the graph
graphs, _ = dgl.load_graphs("movie_graph.bin")
g = graphs[0]

# print("DEBUG:    Node types in graph:", g.ntypes)
# print("DEBUG:   Graph edges:", g.etypes)
# for etype in g.etypes:
#     print(f"DEBUG:   Edge type {etype}: {g.num_edges(etype)} edges")


# Define feature dimension
in_dim = 128

# Initialize random features for each node type
node_features = {
    'movie': torch.randn(g.num_nodes('movie'), in_dim, requires_grad=True),
    'genre': torch.randn(g.num_nodes('genre'), in_dim, requires_grad=True),
    'director': torch.randn(g.num_nodes('director'), in_dim, requires_grad=True),
    'actor': torch.randn(g.num_nodes('actor'), in_dim, requires_grad=True),
}
#print("DEBUG:   Node features available:", node_features.keys())

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
        #print("DEBUG:   Input node features:", {k: v.shape for k, v in inputs.items()})

        h = self.conv1(g, inputs)
        #print("DEBUG:   Output after conv1:", {k: v.shape for k, v in h.items() if v is not None})

        h = {k: torch.relu(v) for k, v in h.items() if v is not None}  # Avoid None values
        h = self.conv2(g, h)
        
        #print("DEBUG:   Output after conv2:", {k: v.shape for k, v in h.items() if v is not None})

        return h
# Initialize the model
rel_names = g.etypes  # e.g., ['belongs_to', 'directed_by', 'features']
# print("DEBUG: Relations processed by HeteroGraphConv:", rel_names)
hidden_dim = 64
out_dim = 32
model = HeteroGNN(in_dim, hidden_dim, out_dim, rel_names)

# Optimizer
optimizer = optim.Adam(model.parameters(), lr=0.01)
num_epochs = 50

# Contrastive Loss (Positive samples should be closer than negative)
def contrastive_loss(pos_sim, neg_sim, margin=1.0):
    return torch.mean(F.relu(margin - pos_sim + neg_sim))

# for ntype in g.ntypes:
#     print(f"DEBUG:   {ntype} has {g.num_nodes(ntype)} nodes.")
#     if g.num_nodes(ntype) > 0:
#         print(f"DEBUG:   {ntype} average in-degree:", g.in_degrees(etype=rel_names[0]).float().mean())
        
for epoch in range(num_epochs):
    model.train()
    embeddings = model(g, node_features)
    # print("DEBUG:   Model output keys:", embeddings.keys())

    # Extract movie embeddings
    movie_emb = embeddings['movie']

    # Generate positive and negative pairs
    num_movies = movie_emb.shape[0]
    positive_pairs = torch.randint(0, num_movies, (10,))  # Random movie indices
    negative_pairs = torch.randint(0, num_movies, (10,))  # Random different movies

    pos_sim = F.cosine_similarity(movie_emb[positive_pairs], movie_emb[positive_pairs])
    neg_sim = F.cosine_similarity(movie_emb[positive_pairs], movie_emb[negative_pairs])

    loss = contrastive_loss(pos_sim, neg_sim)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")

# Save the trained model
torch.save(model.state_dict(), "hetero_gnn_model.pth")
print("DEBUG: Model saved as 'hetero_gnn_model.pth'")
# Extract final node embeddings
embeddings = model(g, node_features)

# Save embeddings for movie recommendations
torch.save(embeddings['movie'], "movie_embeddings.pth")
print("DEBUG: Movie embeddings saved as 'movie_embeddings.pth'")