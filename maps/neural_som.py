import numpy as np

class SimpleSOM:
    def __init__(self, input_dim, num_clusters=2, alpha=0.3, epochs=30):
        self.weights = np.random.rand(num_clusters, input_dim)
        self.alpha = alpha
        self.epochs = epochs

    def winner(self, sample):
        distances = np.linalg.norm(self.weights - sample, axis=1)
        return np.argmin(distances)

    def update(self, sample, winner_idx):
        self.weights[winner_idx] += self.alpha * (sample - self.weights[winner_idx])

    def train(self, data):
        for epoch in range(self.epochs):
            for sample in data:
                winner_idx = self.winner(sample)
                self.update(sample, winner_idx)
            self.alpha *= 0.5

    def predict(self, sample):
        return self.winner(sample)
