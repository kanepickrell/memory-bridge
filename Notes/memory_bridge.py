import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import os
from datetime import datetime

file_path = "memory_bank.json"  # Change this to the actual path if needed

def load_data():
    """
    Loads and returns JSON data from file_path.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def create_graph(data):
    """
    Builds and returns a NetworkX graph (G) along with node_colors, node_sizes, and node_labels.
    """
    # Convert each node category (people, events, locations) into DataFrames
    df_people = pd.DataFrame(data.get("people", []))
    df_events = pd.DataFrame(data.get("events", []))
    df_locations = pd.DataFrame(data.get("locations", []))
    
    # Tag each node type for coloring/labeling
    if not df_people.empty:
        df_people["type"] = "person"
        df_people["label"] = df_people["name"] + " (" + df_people["relationship"] + ")"
    if not df_events.empty:
        df_events["type"] = "event"
        df_events["label"] = df_events["description"]
    if not df_locations.empty:
        df_locations["type"] = "location"
        df_locations["label"] = df_locations["name"]
    
    # Combine all node data into a single DataFrame
    all_nodes = pd.concat([df_people, df_events, df_locations], ignore_index=True, sort=False)
    
    # Create the graph
    G = nx.Graph()
    
    # Define color mapping for each node type
    color_map = {
        "person": sns.color_palette("coolwarm", 3)[1],    # or pick a color you like
        "event": sns.color_palette("coolwarm", 3)[0],
        "location": sns.color_palette("coolwarm", 3)[2]
    }
    
    node_colors = {}
    node_sizes = {}
    node_labels = {}
    
    # Add nodes to the graph
    for _, row in all_nodes.iterrows():
        node_id = row["id"]
        node_type = row["type"]
        recall_strength = row.get("recall_strength", 1)
        label = row["label"]
        
        # Add the node to the graph
        G.add_node(node_id, type=node_type)
        
        # Store label for drawing
        node_labels[node_id] = label
        
        # Assign color and size
        node_colors[node_id] = color_map.get(node_type, "gray")
        node_sizes[node_id] = recall_strength * 600  # Tweak multiplier as you like
    
    # Add edges from the "connections" array
    df_connections = pd.DataFrame(data.get("connections", []))
    
    for _, row in df_connections.iterrows():
        source = row["source"]
        target = row["target"]
        edge_strength = row.get("recall_strength", 1)
        
        # Add edge with weight
        G.add_edge(source, target, weight=edge_strength * 5)
    
    return G, node_colors, node_sizes, node_labels

def draw_graph(ax, G, node_colors, node_sizes, node_labels):
    """
    Draws the graph with improved node spacing to reduce overlap.
    """
    ax.clear()
    ax.set_facecolor("black")  # Set background to black

    # Increase spacing using `k` parameter (higher values spread nodes out)
    pos = nx.spring_layout(G, seed=42, k=.5, scale=1.5)  

    # Alternative: Kamada-Kawai layout (better for small graphs)
    # pos = nx.kamada_kawai_layout(G)

    # Extract edge weights for edge thickness
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

    # Draw edges with thickness based on recall strength
    nx.draw_networkx_edges(
        G, pos, ax=ax, width=edge_weights, alpha=0.5, edge_color="#A9A9A9"
    )

    # Draw nodes with color, size, and white border
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_size=[node_sizes.get(n, 300) for n in G.nodes()],
        node_color=[node_colors.get(n, "gray") for n in G.nodes()],
        edgecolors="white"
    )

    # Draw labels slightly above the node to reduce overlap
    # label_pos = {k: (v[0], v[1] + 0.05) for k, v in pos.items()}
    label_pos = {k: (v[0], v[1] + 0.08) for k, v in pos.items()}  # Moves labels up

    nx.draw_networkx_labels(
        G, label_pos, labels=node_labels, ax=ax,
        font_size=9, font_color="white", font_weight="bold"
    )

    ax.set_title("Exploring & Improving Memory Map", fontsize=14, color="white")
    ax.axis("off")


def update_graph(frame, ax):
    """
    Animation update function: reloads data and redraws the graph.
    """
    data = load_data()
    if data:
        G, node_colors, node_sizes, node_labels = create_graph(data)
        draw_graph(ax, G, node_colors, node_sizes, node_labels)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("black")  # Ensure the figure background is black
    
    # Use FuncAnimation to periodically update the graph (e.g., every 2 seconds)
    ani = animation.FuncAnimation(fig, update_graph, fargs=(ax,), interval=250)
    plt.show()
