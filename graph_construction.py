import pandas as pd
import networkx as nx
import ctypes
ctypes.CDLL("C:/Users/izayo/anaconda3/envs/py310/lib/site-packages/dgl/dgl.dll")
import dgl
import torch
import itertools

# Load cleaned data
df = pd.read_csv("cleaned_movies.csv")

# Extract unique nodes
movies = df["movie_id"].unique()
genres = set(genre for sublist in df["genre"].dropna() for genre in sublist)  # Flatten genre list
directors = df["director_id"].unique()
actors = df["star_id"].unique()

# Create mappings (indexing for fast access)
movie2idx = {m: i for i, m in enumerate(movies)}
genre2idx = {g: i + len(movies) for i, g in enumerate(genres)}
director2idx = {d: i + len(movies) + len(genres) for i, d in enumerate(directors)}
actor2idx = {a: i + len(movies) + len(genres) + len(directors) for i, a in enumerate(actors)}

# Create edges
movie_genre_edges = [(movie2idx[row["movie_id"]], genre2idx[genre]) for _, row in df.iterrows() if isinstance(row["genre"], list) for genre in row["genre"]]
movie_director_edges = [(movie2idx[row["movie_id"]], director2idx[row["director_id"]]) for _, row in df.iterrows()]
movie_actor_edges = [(movie2idx[row["movie_id"]], actor2idx[row["star_id"]]) for _, row in df.iterrows()]

# Optional: Create similarity edges (e.g., movies with the same genre & close ratings)
similar_movie_edges = []
for genre in genres:
    similar_movies = df[df["genre"].apply(lambda x: genre in x)]["movie_id"].tolist()
    pairs = list(itertools.combinations(similar_movies, 2))  # Pairwise movie connections
    similar_movie_edges.extend([(movie2idx[a], movie2idx[b]) for a, b in pairs])

# Create DGL graph
graph_data = {
    ('movie', 'belongs_to', 'genre'): torch.tensor(movie_genre_edges, dtype=torch.int64).T,
    ('movie', 'directed_by', 'director'): torch.tensor(movie_director_edges, dtype=torch.int64).T,
    ('movie', 'features', 'actor'): torch.tensor(movie_actor_edges, dtype=torch.int64).T,
    ('movie', 'similar_to', 'movie'): torch.tensor(similar_movie_edges, dtype=torch.int64).T
}

# Build the heterogeneous graph
g = dgl.heterograph(graph_data)

# Save the graph
dgl.save_graphs("movie_graph.bin", g)

print(g)
