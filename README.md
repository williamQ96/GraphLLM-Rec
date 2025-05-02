# GraphLLM-Rec

---

A hybrid movie recommendation system that combines graph-based collaborative filtering with LLM‑driven preference refinement. This repo implements two recommender variants—reco2 (supports user dislikes) and the original recommand—and provides both batch and interactive UIs.

---

## 🚀 Features

### Graph Construction & Embedding

- Build a user–movie heterogeneous graph from cleaned CSV data (cleaned_movies.csv).

- Generate node embeddings via a GNN model (hetero_gnn_model.pth).

### Dual Recommender Engines

- Reco2: Handles user dislikes gracefully (empty or populated lists).

- Recommand: Original collaborative filtering baseline.

### LLM Preference Enhancement

- Extract nuanced likes/dislikes from free‑form text (optional; not shown here).

### Interactive Web UI

- Flask app (app.py) serving templates (templates/) and static assets (static/).

- Command‑line interface via recforuser.py.

---

### 📁 Repository Structure

GraphLLM-Rec/

├── .idea/                         # IDE settings (ignore in Git)

├── __pycache__/                   # Python cache (ignore in Git)

├── data/                          # Raw and intermediate CSV datasets

├── movie_data/                    # Original MovieLens files

├── cleaned_movies.csv             # Preprocessed movie metadata

├── filter­ing.py                  # Filtering utilities for rating thresholds

├── graph_construction.py          # Build and serialize movie graph

├── visualize_graph.py             # Tool to visualize graph structure

├── model.py                       # GNN model definition & training script

├── hetero_gnn_model.pth           # Trained GNN model weights

├── movie_embeddings.pth           # Saved node embeddings

├── movie_graph.bin                # Serialized graph object

├── reco2.py                       # Second recommender (handles dislikes)

├── reco2backup.py                 # Previous version of reco2

├── recommand.py                   # Original recommender implementation

├── recforuser.py                  # CLI for generating recommendations

├── recommand_ui.py                # Web UI integration for recommendations

├── id_to_name.py                  # Utility: map internal IDs to IMDb titles

├── node_index_to_imdb.json        # Mapping of graph node indices to IMDb IDs

├── user_profiles.py               # Load and manage user profile data

├── user_data.json                 # Sample user profiles & preferences

├── version.py                     # Project version and metadata

├── app.py                         # Flask entry point for interactive demo

├── static/                        # CSS, JS, images for web UI

│   └── placeholder.png            # Default movie poster placeholder

├── templates/                     # HTML templates for Flask app

├── log.md                         # Development and change log

├── README.md                      # This file

└── requirements.txt               # Python dependencies

Note: .idea/ and __pycache__/ are included by your IDE/Python; please add them to .gitignore before publishing.

---

## 🔧 Installation & Setup

### Clone the repository

```git clone https://github.com/your-username/GraphLLM-Rec.git```

```cd GraphLLM-Rec```

### Create and activate a virtual environment

```python3 -m venv venv```

```source venv/bin/activate      # macOS/Linux```

```venv\Scripts\activate.bat   # Windows```

### Install dependencies

```pip install -r requirements.txt```

```python -m nltk.downloader punkt wordnet```

#### Prepare data

#### Place raw MovieLens files in movie_data/, or let filtering.py download them.

#### Run preprocessing:

```python filtering.py```

```python graph_construction.py```

#### Train (or load) the GNN:

```python model.py```

---

## 🏃‍♂️ Usage

### Batch recommendations (CLI):

```python recforuser.py --user-id 123 --engine reco2```

### Interactive web demo:

```python app.py```

### Then open http://localhost:5000 in your browser

---

## 🤝 Contributing

- Contributions are welcome! Please:

- Fork the repo

- Create a feature branch (git checkout -b feature/YourFeature)

- Commit your changes (git commit -m "Add awesome feature")

- Push to the branch (git push origin feature/YourFeature)

- Open a Pull Request

- Please follow the Contributor Covenant.

---

## 📄 License

- This project is licensed under the MIT License. See LICENSE for details.
