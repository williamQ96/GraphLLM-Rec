import pandas as pd
import networkx as nx
import dgl
import torch

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
