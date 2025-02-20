import dgl
import torch
import networkx as nx
import matplotlib.pyplot as plt

# Load the graph
graph_list, _ = dgl.load_graphs("movie_graph.bin")
g = graph_list[0]  # Assuming there is only one graph

print("Loaded Graph:")
print(g)

# Convert DGL graph to NetworkX for visualization
def visualize_dgl_graph(dgl_graph, edge_type=None, max_nodes=100):
    """
    Visualizes a DGL graph using NetworkX.
    
    Parameters:
        dgl_graph: DGLGraph - The heterogeneous graph
        edge_type: tuple - Edge type to visualize (optional)
        max_nodes: int - Max number of nodes to plot for clarity
    """
    if edge_type:
        src, dst = dgl_graph.edges(etype=edge_type)
    else:
        src, dst = dgl_graph.edges()

    # Convert to NetworkX
    nx_graph = nx.Graph()
    for s, d in zip(src.tolist(), dst.tolist()):
        nx_graph.add_edge(s, d)

    # Limit number of nodes for visualization
    if nx_graph.number_of_nodes() > max_nodes:
        subgraph_nodes = list(nx_graph.nodes)[:max_nodes]
        nx_graph = nx_graph.subgraph(subgraph_nodes)

    # Draw the graph
    plt.figure(figsize=(10, 8))
    nx.draw(nx_graph, with_labels=False, node_size=50, edge_color="gray", alpha=0.6)
    plt.title(f"Visualization of {'all edges' if not edge_type else edge_type} (max {max_nodes} nodes)")
    plt.show()

# Visualize a subgraph (e.g., movies and genres)
visualize_dgl_graph(g, edge_type=('movie', 'belongs_to', 'genre'))
