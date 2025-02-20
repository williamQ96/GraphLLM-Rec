import pandas as pd
import networkx as nx
import dgl
import torch
# torch.set_num_threads(1)
import matplotlib.pyplot as plt
# import os
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Load cleaned data
df = pd.read_csv("cleaned_movies.csv")

# Ensure genres are lists (fix if stored as strings)
df["genre"] = df["genre"].apply(lambda x: eval(x) if isinstance(x, str) else x)

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
movie_genre_edges = [(movie2idx[row["movie_id"]], genre2idx[genre]) 
                     for _, row in df.iterrows() if isinstance(row["genre"], list) for genre in row["genre"]]

movie_director_edges = [(movie2idx[row["movie_id"]], director2idx[row["director_id"]]) 
                        for _, row in df.iterrows() if row["director_id"] in director2idx]

movie_actor_edges = [(movie2idx[row["movie_id"]], actor2idx[row["star_id"]]) 
                     for _, row in df.iterrows() if row["star_id"] in actor2idx]



print("Movie-Genre Edge Format:", type(movie_genre_edges), len(movie_genre_edges), movie_genre_edges[:5])
print("Movie-Director Edge Format:", type(movie_director_edges), len(movie_director_edges), movie_director_edges[:5])
print("Movie-Actor Edge Format:", type(movie_actor_edges), len(movie_actor_edges), movie_actor_edges[:5])


# Create DGL graph
def prepare_edge_list(edge_list):
    if edge_list and all(len(edge) == 2 for edge in edge_list):  # Ensure edge_list is not empty and has valid pairs
        src, dst = zip(*edge_list)  # Unzipping into two lists
        return list(src), list(dst)  # Return as tuple of two lists
    else:
        return [], []  # If empty, return empty lists
    
graph_data = {
    ('movie', 'belongs_to', 'genre'): prepare_edge_list(movie_genre_edges),
    ('movie', 'directed_by', 'director'): prepare_edge_list(movie_director_edges),
    ('movie', 'features', 'actor'): prepare_edge_list(movie_actor_edges),
}

# for key, value in graph_data.items():
#     print(f"Edge Type: {key}")
#     print("Data Type:", type(value))

# Build the heterogeneous graph
g = dgl.heterograph(graph_data)

# Save the graph
dgl.save_graphs("movie_graph.bin", g)


print("Constructed DGL Graph:")
print(g)
print("Graph construction complete!")
