import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import networkx as nx
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib.widgets import Button

# ---------------------------
# Data Generation and Preprocessing
# ---------------------------

people = ["Frank", "Lisa", "Tim", "Joe"]
places = ["Beach", "Paris", "Vegas", "Tennessee", "Dayton", "Coffee Shop", "Iceland", "San Antonio"]
events = ["Vacation", "Graduation", "Wedding", "Basketball", "Fishing", "Hiking", "Sleeping", "Running"]
times = ["1998", "two years ago", "Childhood", "Last Year", "This Year", "2001", "2015", "March", "July"]

actions = [
    "went to", "enjoyed", "visited", "spent time at",
    "had a memorable", "experienced", "took a trip to",
    "attended", "organized", "celebrated"
]

descriptions = [
    "beautiful weather", "an exciting adventure", "a relaxing weekend",
    "an unforgettable night", "great company", "lots of fun",
    "a peaceful day", "an energetic atmosphere"
]

def generate_conway_memory_dataset(n=100):
    data = []
    for _ in range(n):
        action = random.choice(actions)
        event = random.choice(events)
        person = random.choice(people)
        place = random.choice(places)
        time = random.choice(times)
        description = random.choice(descriptions)

        sentence_structure = random.choice([
            f"{person} and I {action} {place} for {event} in {time}",
            f"{event} at {place} with {person} was {description}",
            f"In {time}, {person} and I had {description} during our {event}",
            f"I {action} {event.lower()} in {place} alongside {person}",
            f"{place} was where {person} and I {action} {description}"
        ])

        data.append([sentence_structure, person, place, event, time])
        
    df = pd.DataFrame(data, columns=["Memory", "Person", "Place", "Event", "Time"])
    return df.sample(frac=1).reset_index(drop=True)

# Generate a dataset of 100 memories
dataset = generate_conway_memory_dataset(100)

model = SentenceTransformer('all-MiniLM-L6-v2')
text_embeddings = model.encode(dataset["Memory"].tolist())

pca = PCA(n_components=4)
reduced_embeddings = pca.fit_transform(text_embeddings)

# ---------------------------
# Online SOM Implementation
# ---------------------------

class OnlineSOM:
    def __init__(self, m, n, input_dim, learning_rate=0.1, sigma=1.0):
        self.m = m
        self.n = n
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.sigma = sigma
        self.weights = np.random.random((m, n, input_dim))

    def get_bmu(self, sample):
        distances = np.linalg.norm(self.weights - sample, axis=2)
        return np.unravel_index(np.argmin(distances), distances.shape)

    def update(self, sample):
        bmu_index = self.get_bmu(sample)
        for i in range(self.m):
            for j in range(self.n):
                neuron_location = np.array([i, j])
                dist_to_bmu = np.linalg.norm(neuron_location - bmu_index)
                h = np.exp(-dist_to_bmu**2 / (2 * (self.sigma ** 2)))
                self.weights[i, j, :] += self.learning_rate * h * (sample - self.weights[i, j, :])
        return bmu_index

som = OnlineSOM(m=4, n=4, input_dim=4, learning_rate=0.1, sigma=1.0)

memory_records = []
bmu_assignments = []
stream_data = reduced_embeddings

# Setup plot
fig, ax = plt.subplots(1, 2, figsize=(15, 8))
plt.subplots_adjust(bottom=0.2)
current_idx = [0]

def update_plot(event):
    if current_idx[0] >= len(stream_data):
        return

    sample = stream_data[current_idx[0]]
    bmu = som.update(sample)
    bmu_assignments.append(bmu)
    memory_records.append(dataset["Memory"].iloc[current_idx[0]])
    current_idx[0] += 1

    ax[0].clear()
    ax[1].clear()

    neuron_positions = np.array([[i, j] for i in range(som.m) for j in range(som.n)])
    ax[0].scatter(neuron_positions[:, 0], neuron_positions[:, 1], s=150, c='red', marker='s', label='Neurons')

    bmu_array = np.array(bmu_assignments)
    jitter = np.random.normal(0, 0.1, bmu_array.shape)
    points = bmu_array + jitter
    ax[0].scatter(points[:, 0], points[:, 1], s=50, c='blue', label='Memory BMUs')
    ax[0].set_title("SOM Grid & Memory BMU Mapping")
    ax[0].set_xlim(-1, som.m)
    ax[0].set_ylim(-1, som.n)
    ax[0].legend()

    if len(memory_records) > 1:
        current_embeddings = stream_data[:current_idx[0]]
        similarity_matrix = cosine_similarity(current_embeddings)
        G = nx.Graph()
        for i in range(len(current_embeddings)):
            G.add_node(i, label=memory_records[i])
        for i in range(len(current_embeddings)):
            for j in range(i+1, len(current_embeddings)):
                if similarity_matrix[i, j] > 0.7:
                    G.add_edge(i, j, weight=similarity_matrix[i, j])
        pos = nx.spring_layout(G, k=0.5, seed=42)
        nx.draw(G, pos, ax=ax[1], with_labels=True, labels=nx.get_node_attributes(G, 'label'), node_size=300, node_color='skyblue', font_size=7)
        ax[1].set_title("Memory Similarity Network")

    plt.draw()

ax_next = plt.axes([0.45, 0.05, 0.1, 0.075])
bnext = Button(ax_next, 'Next')
bnext.on_clicked(update_plot)

plt.show()