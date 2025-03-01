import pandas as pd
import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import os

file_path = "memory_bank.json"  # Change this to the actual path if needed

def load_data():
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def create_graph(data):
    df_people = pd.json_normalize(data, record_path=['people'])
    df_events = pd.json_normalize(data, record_path=['events'])
    df_locations = pd.json_normalize(data, record_path=['locations'])
    
    df_events = df_events.explode('related_people')
    df_events[['person_id', 'person_recall_strength']] = pd.DataFrame(df_events['related_people'].tolist(), index=df_events.index)
    df_events.drop(columns=['related_people'], inplace=True)
    
    df_merged = df_events.merge(df_people, left_on='person_id', right_on='id', how='left', suffixes=('_event', '_person'))
    df_merged = df_merged.explode('related_places')
    df_merged[['location_id', 'location_recall_strength']] = pd.DataFrame(df_merged['related_places'].tolist(), index=df_merged.index)
    df_merged.drop(columns=['related_places'], inplace=True)
    df_merged = df_merged.merge(df_locations, left_on='location_id', right_on='id', how='left', suffixes=('', '_location'))
    
    G = nx.Graph()
    node_colors = {}
    node_sizes = {}
    color_palette = {"event": "#FF4500", "person": "#00CED1", "location": "#FFD700"}

    for _, row in df_merged.iterrows():
        event_node = f"{row['description_event']}"
        person_node = f"{row['name']} ({row['relationship']})"
        location_node = f"{row['name_location']}"

        G.add_node(event_node, type="event")
        G.add_node(person_node, type="person")
        G.add_node(location_node, type="location")

        node_colors[event_node] = color_palette["event"]
        node_colors[person_node] = color_palette["person"]
        node_colors[location_node] = color_palette["location"]

        node_sizes[event_node] = row.get('recall_strength_event', 1) * 800
        node_sizes[person_node] = row.get('recall_strength_person', 1) * 600
        node_sizes[location_node] = row.get('recall_strength', 1) * 700

        G.add_edge(event_node, person_node, weight=row.get('recall_strength_event', 1) * 5)
        G.add_edge(event_node, location_node, weight=row.get('location_recall_strength', 1) * 5)
    
    return G, node_colors, node_sizes

def draw_graph(ax, G, node_colors, node_sizes):
    ax.clear()
    ax.set_facecolor("black")  # Set background to black
    pos = nx.spring_layout(G, seed=63)
    edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, ax=ax, width=edge_weights, alpha=0.5, edge_color="#A9A9A9")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[node_sizes.get(n, 500) for n in G.nodes()],
                           node_color=[node_colors.get(n, "gray") for n in G.nodes()], edgecolors="white")
    label_pos = {k: (v[0], v[1] + 0.04) for k, v in pos.items()}
    nx.draw_networkx_labels(G, label_pos, ax=ax, font_size=9, font_color="white", font_weight="bold")
    ax.set_title("Node Map", fontsize=14, color="white")
    ax.axis("off")

def update_graph(frame, ax):
    data = load_data()
    if data:
        G, node_colors, node_sizes = create_graph(data)
        draw_graph(ax, G, node_colors, node_sizes)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(12, 10))
    fig.patch.set_facecolor("black")  # Ensure the full figure background is black
    ani = animation.FuncAnimation(fig, update_graph, fargs=(ax,), interval=5000)  # Update every 5 seconds
    plt.show()