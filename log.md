2.2 Data Preprocessing
Cleaning & Filtering:
Remove missing/null values.
Standardize movie titles and names.

Graph Construction:
Define nodes: Movies, Users (if applicable), Genres, Actors, Directors.
Define edges: Relationships between nodes (e.g., movie-actor, movie-genre).

Feature Engineering:
Encode categorical features (e.g., movie genres).
Normalize numerical features (e.g., ratings).
Generate user embeddings (if collaborative filtering is involved).


2/18

we have clean data.
flitering out duplicated, and customized rule(df["votes"] >= 100) & (df["rating"] >= 3.0)

heterogeneous graph

1.1 Node Types
Each node represents an entity:

Movie Nodes (movie_id)
Genre Nodes (genre)
Actor Nodes (star_id)
Director Nodes (director_id)
1.2 Edge Types (Relationships)
Each edge represents a relationship between entities:

(Movie) → belongs to → (Genre)
(Movie) → directed by → (Director)
(Movie) → features → (Actor)
(Movie) → similar_to → (Movie) (optional, based on similarity)

