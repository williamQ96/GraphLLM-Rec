
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

_______________________________________________________________________________
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
_______________________________________________________________________________

2/19:
ideas:
    incorporate deepseek to understand comments.
        LLM Cold start option. 
        "AI summary" like amazon items.
    “Highest-grossing films adjusted for inflation” https://en.wikipedia.org/wiki/List_of_highest-grossing_films 

Questions:
    how to test for effectiveness
        Interpretability & Explainability
            Can the system explain why it recommended an item?
            Trust in the system increases if users understand the logic behind recommendations.
                Understanding Model Behavior

                    Since you don’t have historical data, you likely don’t have ground-truth labels to measure accuracy in the traditional sense. Being able to explain recommendations helps you verify if your system is making reasonable choices.
                    Debugging & Improving the Model

                    If recommendations don’t make sense, an explainable model helps pinpoint where things might be going wrong. Are the recommendations dominated by certain features? Are they biased toward specific types of inputs?
                    User Trust & Human Evaluation

                    If your project involves user testing (e.g., asking students to interact with the system), explaining why recommendations were made can help collect more meaningful feedback.
                    Academic & Presentation Value

                    A well-explained model is easier to present and defend in a class project. It shows that you understand the inner workings of the recommender, rather than just running an algorithm blindly.
                    How to Implement Interpretability in Your Project
                    Feature Contribution Analysis

                    If you're using a content-based recommender, you can show which features influenced the recommendation the most.
                    Example: "This movie was recommended because you liked Sci-Fi and it has a high IMDb rating."
                    Similarity Scores (for Collaborative or Content-Based Filtering)

                    Show why an item was recommended by displaying similarity scores.
                    Example: "This book was recommended because it has a 75% similarity with a book you rated highly."
                    Visualization Techniques

                    t-SNE or PCA: If using an embedding-based approach (like word2vec for items), visualize the embeddings to show how items cluster.
                    Decision Trees (if using a rule-based approach): Show which rules were used for recommendations.
                    Shapley Values (SHAP)

                    If using a machine learning-based approach (e.g., a neural network or decision tree model), SHAP can break down how much each feature contributed to the final recommendation.
                    Human Evaluation

                    Ask test users (even if just classmates) to rate whether the explanations make sense.
                    Example: Show the top 3 reasons why a recommendation was made and ask users if they agree with the reasoning.
    need for GUI?
            OpenUI:
    
Resources:
    the movie DB
        https://www.themoviedb.org/
    Alibaba EasyRec 
        https://github.com/alibaba/EasyRec
    A list of recommander system repo:
        https://github.com/grahamjenson/list_of_recommender_systems
    Movie recommander with GUI
        https://github.com/shyam1998/Movie-Recommendation-System-GUI
    OpenUI:
        https://github.com/wandb/openui
    Minimind:
        https://github.com/jingyaogong/minimind
    Monolith:
        https://github.com/bytedance/monolith  
    GraphRag:
        https://github.com/microsoft/graphrag
_______________________________________________________________________________

2/20
    graph is constructed
        but visualization has problem.

    Next up:
        fix visualization
        ready to train

2/21 
    vLLM api
        can be used for ai app.

    LLM in Feature Augmentation for Recommendation Systems
        LLM as a feature enhancer rather than a direct recommender.
        LLM-based prediction: Generates recommendations based on existing reviews made by the user.
        LLM as a feature converter: Processes reviews to enhance recommendation quality.
        
    Cold Start Scenarios:
    Basic cold start: traditional pick&choice,
        or, input a natural language paragraph and LLM make prediction base on the text. 

    Memory-based improvement: Enhances recommendations through user interaction over time.

    LLM -> feature augmentation
        LLM prediction based on review -> recommander system
        LLM as a feature converter, instead of direct recommander directly.

            
