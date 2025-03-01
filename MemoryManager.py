import json
from pprint import pprint
from collections import namedtuple

Node = namedtuple(
    "Node",
    ["id", "name", "type", "tags", "recall_strength"],
    defaults=[[], 0.5]
)
Link = namedtuple("Link", ["source", "target", "strength"])

class MemoryAccess:
    def __init__(self, filename):
        self.filename = filename
        self.nodes = []
        self.links = []
        self.load_data()

    def load_data(self):
        with open(self.filename, "r", encoding='utf-8') as file:
            data = json.load(file)

        self.nodes = [
            Node(
                **{
                    "id": node["id"],
                    "name": node["name"],
                    "type": node["type"],
                    "tags": node.get("tags", []),
                    "recall_strength": node.get("recall_strength", 0.5)
                }
            )
            for node in data.get("nodes", [])
        ]

        self.links = [Link(**link) for link in data.get("links", [])]

    def save_data(self):
        data = {
            "nodes": [node._asdict() for node in self.nodes],
            "links": [link._asdict() for link in self.links]
        }
        with open(self.filename, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def get_highest_recall_memories(self, top_n=2):
        sorted_nodes = sorted(self.nodes, key=lambda node: node.recall_strength, reverse=True)
        return sorted_nodes[:top_n]
    
    def increase_recall(self, node_id):
        for idx, node in enumerate(self.nodes):
            if node.id == node_id:
                # Increase recall_strength by 0.1, ensuring it doesn't exceed 1.0
                new_strength = min(node.recall_strength + 0.1, 1.0)
                # Create a new Node with the updated recall_strength
                self.nodes[idx] = node._replace(recall_strength=new_strength)
                print(f"Updated node {node_id}: recall_strength from {node.recall_strength} to {new_strength}")
                break
        else:
            print(f"Node with id {node_id} not found.")

if __name__ == "__main__":
    json_filename = "C:/repos/memory-bridge/frontend/src/data.json" 
    memory_map = MemoryAccess(json_filename)

    top_memories = memory_map.get_highest_recall_memories()

    print("Top memory(ies) based on recall strength:")
    for memory in top_memories:
        pprint(memory._asdict())
