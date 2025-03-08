import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from neural_som import SimpleSOM
from som_memories_g import generate_conway_memory_dataset, generate_lifetime_dataset


# Generate Conway-style dataset
conway_memory_dataset = generate_lifetime_dataset(10)
print("Conway Memory Dataset:")
print(conway_memory_dataset.head(10))

model = SentenceTransformer('all-MiniLM-L6-v2')
memory_embeddings = model.encode(conway_memory_dataset["Memory"])

# PCA Dimensionality Reduction
pca = PCA(n_components=4)
reduced_embeddings = pca.fit_transform(memory_embeddings)

# Train the self-organizing map
som = SimpleSOM(input_dim=4, num_clusters=2, alpha=0.3, epochs=30)
som.train(reduced_embeddings)

clusters = [som.predict(sample) for sample in reduced_embeddings]
conway_memory_dataset['Predicted Cluster'] = clusters

similarity_matrix = cosine_similarity(memory_embeddings)
G = nx.Graph()

for idx, memory in enumerate(conway_memory_dataset['Memory']):
    G.add_node(idx, label=memory)

threshold = 0.8
for i in range(len(similarity_matrix)):
    for j in range(i + 1, len(similarity_matrix)):
        if similarity_matrix[i, j] > threshold:
            G.add_edge(i, j, weight=similarity_matrix[i, j])

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, k=0.5)
nx.draw(G, pos, with_labels=True, labels=nx.get_node_attributes(G, 'label'),
        node_size=300, node_color='skyblue', font_size=5, font_weight='bold')
plt.title('Conway Memory Network Visualization')
plt.show()


