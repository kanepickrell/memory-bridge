import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Compute pairwise similarity clearly
similarity_matrix = cosine_similarity(memory_embeddings)

# Build network
G = nx.Graph()

# Add nodes (memories)
for idx, memory in enumerate(text_memory_dataset['Memory']):
    G.add_node(idx, label=memory)

# Add edges clearly (threshold-based)
threshold = 0.8
for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        if similarity_matrix[i, j] > threshold:
            G.add_edge(i, j, weight=similarity_matrix[i, j])

# Visualize
pos = nx.spring_layout(G, k=0.5)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=3000, node_color='lightblue', font_size=10)
plt.show()
