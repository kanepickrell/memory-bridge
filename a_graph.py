import networkx as nx
from pyvis.network import Network
import random
import time
import math
import webbrowser
import os
from IPython.display import IFrame, display, HTML

class MemoryNode:
    """Represents a single memory node in the memory graph"""
    def __init__(self, id, label, node_type, hierarchy_level, initial_confidence=0.6):
        self.id = id
        self.label = label
        self.type = node_type  # person, place, event, emotion
        self.hierarchy_level = hierarchy_level  # lifetime_period, general_event, specific_detail
        self.storage_strength = initial_confidence  # how well stored in long-term memory
        self.retrieval_strength = initial_confidence * 0.8  # how easily retrieved
        self.verified = False  # whether verified by family
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.recall_history = []  # track recall successes/failures
    
    def get_size(self):
        """Determine visual size based on memory strength"""
        base_size = 15
        strength_factor = 25
        recency_boost = 10 * math.exp(-(time.time() - self.last_accessed) / 60)
        return base_size + (self.retrieval_strength * strength_factor) + recency_boost
    
    def get_color(self):
        """Get color based on node type and retrieval strength"""
        # Base colors for different node types
        type_colors = {
            "person": "rgba(41, 128, 185, {opacity})",  # blue
            "place": "rgba(39, 174, 96, {opacity})",    # green
            "event": "rgba(142, 68, 173, {opacity})",   # purple
            "emotion": "rgba(231, 76, 60, {opacity})",  # red
            "object": "rgba(243, 156, 18, {opacity})"   # orange
        }
        
        color_template = type_colors.get(self.type, "rgba(149, 165, 166, {opacity})")
        opacity = 0.4 + (self.retrieval_strength * 0.6)  # Range from 0.4 to 1.0
        
        return color_template.format(opacity=opacity)
    
    def get_border_width(self):
        """Get border width based on verification status"""
        return 3 if self.verified else 1
    
    def get_border_color(self):
        """Get border color based on verification status"""
        return "#FFD700" if self.verified else "#FFFFFF"
    
    def get_hover_text(self):
        """Generate text shown when hovering over this node"""
        status = "Verified" if self.verified else "Unverified"
        
        if self.type == "person":
            return f"<b>{self.label}</b><br>Relationship<br>Recall strength: {int(self.retrieval_strength*100)}%<br>{status}"
        elif self.type == "place":
            return f"<b>{self.label}</b><br>Location<br>Recall strength: {int(self.retrieval_strength*100)}%<br>{status}"
        elif self.type == "event":
            return f"<b>{self.label}</b><br>Event<br>Recall strength: {int(self.retrieval_strength*100)}%<br>{status}"
        else:
            return f"<b>{self.label}</b><br>{self.type.capitalize()}<br>Recall strength: {int(self.retrieval_strength*100)}%<br>{status}"
    
    def recall_success(self, difficulty=1.0):
        """Update strengths after successful recall"""
        # Strengthen both storage and retrieval strength
        self.storage_strength = min(1.0, self.storage_strength + (0.05 * difficulty))
        self.retrieval_strength = min(1.0, self.retrieval_strength + (0.1 * difficulty))
        self.last_accessed = time.time()
        self.recall_history.append(True)
    
    def recall_failure(self):
        """Update strengths after failed recall"""
        # Storage strength is maintained but retrieval strength decreases
        self.retrieval_strength = max(0.1, self.retrieval_strength - 0.15)
        self.last_accessed = time.time()
        self.recall_history.append(False)
    
    def verify(self):
        """Mark memory as verified (e.g., by family input)"""
        self.verified = True
        self.storage_strength = min(1.0, self.storage_strength + 0.2)
        self.retrieval_strength = min(1.0, self.retrieval_strength + 0.1)


class MemoryConnection:
    """Represents a connection between two memory nodes"""
    def __init__(self, source, target, relationship, initial_strength=0.5):
        self.source = source
        self.target = target
        self.relationship = relationship
        self.strength = initial_strength
        self.created_at = time.time()
        self.access_count = 0
    
    def get_width(self):
        """Determine visual width based on connection strength"""
        base_width = 1
        strength_factor = 7
        return base_width + (self.strength * strength_factor)
    
    def get_color(self):
        """Get color based on connection strength"""
        return f"rgba(149, 165, 166, {0.4 + (self.strength * 0.6)})"
    
    def get_hover_text(self):
        """Generate text shown when hovering over this connection"""
        return f"<b>{self.relationship}</b><br>Connection strength: {int(self.strength*100)}%"
    
    def strengthen(self, amount=0.1):
        """Strengthen the connection"""
        self.strength = min(1.0, self.strength + amount)
        self.access_count += 1


class MemoryGraph:
    """Manages the entire memory graph structure"""
    def __init__(self):
        self.graph = nx.Graph()
        self.nodes = {}  # Stores MemoryNode objects
        self.connections = {}  # Stores MemoryConnection objects
        self.user_name = "James"
        self.timestamp = time.time()
    
    def add_node(self, memory_node):
        """Add a new memory node to the graph"""
        self.nodes[memory_node.id] = memory_node
        # Add to networkx graph
        self.graph.add_node(memory_node.id)
    
    def add_connection(self, connection):
        """Add a connection between two memory nodes"""
        # Create a unique ID for the connection
        conn_id = f"{connection.source}_{connection.target}"
        self.connections[conn_id] = connection
        
        # Add to networkx graph
        self.graph.add_edge(
            connection.source, 
            connection.target, 
            relationship=connection.relationship
        )
    
    def get_node(self, node_id):
        """Get a memory node by ID"""
        return self.nodes.get(node_id)
    
    def get_connections_for_node(self, node_id):
        """Get all connections involving this node"""
        result = []
        for conn_id, conn in self.connections.items():
            if conn.source == node_id or conn.target == node_id:
                result.append(conn)
        return result
    
    def strengthen_node_and_connections(self, node_id, difficulty=1.0):
        """Strengthen a node and all its connections (after successful recall)"""
        # Strengthen the node
        node = self.get_node(node_id)
        if node:
            node.recall_success(difficulty)
            
            # Also strengthen all connections to this node
            for conn in self.get_connections_for_node(node_id):
                conn.strengthen(amount=0.08 * difficulty)
    
    def weaken_node(self, node_id):
        """Weaken a node after failed recall"""
        node = self.get_node(node_id)
        if node:
            node.recall_failure()
    
    def verify_node(self, node_id):
        """Mark a memory node as verified (e.g., by family photo)"""
        node = self.get_node(node_id)
        if node:
            node.verify()
            
            # Also strengthen connections to this node
            for conn in self.get_connections_for_node(node_id):
                conn.strengthen(amount=0.15)
    
    def visualize(self, output_file="memory_graph.html", height="750px", width="100%"):
        """Generate an interactive visualization of the memory graph"""
        # Create Pyvis network
        net = Network(height=height, width=width, bgcolor="#222222", font_color="white")
        
        # Add nodes with appropriate styling
        for node_id, node in self.nodes.items():
            net.add_node(
                node_id,
                label=node.label,
                title=node.get_hover_text(),
                size=node.get_size(),
                color=node.get_color(),
                borderWidth=node.get_border_width(),
                borderWidthSelected=node.get_border_width() + 2,
                borderColor=node.get_border_color()
            )
        
        # Add edges with appropriate styling
        for conn_id, conn in self.connections.items():
            net.add_edge(
                conn.source,
                conn.target,
                title=conn.get_hover_text(),
                width=conn.get_width(),
                color=conn.get_color()
            )
        
        # Configure physics and other visual options
        net.set_options("""
        var options = {
          "nodes": {
            "font": {
              "size": 16,
              "face": "Tahoma"
            },
            "shape": "dot"
          },
          "edges": {
            "color": {
              "inherit": false
            },
            "smooth": {
              "type": "continuous",
              "forceDirection": "none"
            }
          },
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -8000,
              "springLength": 150,
              "avoidOverlap": 0.5
            },
            "minVelocity": 0.75,
            "solver": "barnesHut"
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 200
          }
        }
        """)
        
        # Save and display
        net.show(output_file)
        return output_file


# Demo function to show Memory Bridge in action
def run_memory_bridge_demo():
    """Demo showing Memory Bridge's dynamic memory graph in action"""
    # Initialize the memory graph
    memory_graph = MemoryGraph()
    
    # Step 1: Initial conversation and memory formation
    print("Step 1: Initial conversation - James mentions Paris trip")
    
    # Create initial nodes
    paris_trip = MemoryNode("paris_trip", "Paris Trip 1998", "event", "general_event")
    lisa = MemoryNode("lisa", "Lisa", "person", "specific_detail")
    eiffel_tower = MemoryNode("eiffel_tower", "Eiffel Tower", "place", "specific_detail")
    
    # Add nodes to graph
    memory_graph.add_node(paris_trip)
    memory_graph.add_node(lisa)
    memory_graph.add_node(eiffel_tower)
    
    # Create connections
    memory_graph.add_connection(MemoryConnection("paris_trip", "lisa", "traveled with"))
    memory_graph.add_connection(MemoryConnection("paris_trip", "eiffel_tower", "visited"))
    
    # Visualize initial state
    memory_graph.visualize("step1_initial_memory.html")
    print("Initial memory graph created - showing basic connections")
    time.sleep(1)
    
    # Step 2: Memory recall success
    print("\nStep 2: James successfully recalls Lisa was on the Paris trip")
    memory_graph.strengthen_node_and_connections("lisa")
    memory_graph.visualize("step2_recall_success.html")
    print("Graph updated - Lisa node and connections strengthened (notice increased size and brightness)")
    time.sleep(1)
    
    # Step 3: New memory added through conversation
    print("\nStep 3: James mentions they ate at a restaurant near the Eiffel Tower")
    restaurant = MemoryNode("restaurant", "Cafe near Tower", "place", "specific_detail", 0.5)
    memory_graph.add_node(restaurant)
    memory_graph.add_connection(MemoryConnection("paris_trip", "restaurant", "dined at"))
    memory_graph.add_connection(MemoryConnection("eiffel_tower", "restaurant", "located near"))
    memory_graph.visualize("step3_new_memory.html")
    print("Graph updated - New nodes and connections added from conversation")
    time.sleep(1)
    
    # Step 4: Failed recall
    print("\nStep 4: James struggles to remember the name of the restaurant")
    memory_graph.weaken_node("restaurant")
    memory_graph.visualize("step4_failed_recall.html")
    print("Graph updated - Restaurant node shows weaker recall strength (dimmer, smaller)")
    time.sleep(1)
    
    # Step 5: Family verification
    print("\nStep 5: Family uploads a photo of James and Lisa at the Eiffel Tower")
    memory_graph.verify_node("eiffel_tower")
    memory_graph.verify_node("lisa")
    memory_graph.visualize("step5_family_verification.html")
    print("Graph updated - Lisa and Eiffel Tower nodes verified (gold border)")
    time.sleep(1)
    
    # Step 6: Memory rediscovery
    print("\nStep 6: Photo helps James remember they also visited Notre Dame")
    notre_dame = MemoryNode("notre_dame", "Notre Dame", "place", "specific_detail")
    notre_dame.verified = True  # Verified immediately by photo
    memory_graph.add_node(notre_dame)
    memory_graph.add_connection(MemoryConnection("paris_trip", "notre_dame", "visited"))
    
    happy = MemoryNode("happy", "Happiness", "emotion", "specific_detail", 0.7)
    memory_graph.add_node(happy)
    memory_graph.add_connection(MemoryConnection("paris_trip", "happy", "felt"))
    
    # Also add John who was forgotten until now
    john = MemoryNode("john", "John", "person", "specific_detail", 0.4)  # Weak initial memory
    memory_graph.add_node(john)
    memory_graph.add_connection(MemoryConnection("paris_trip", "john", "traveled with"))
    memory_graph.add_connection(MemoryConnection("lisa", "john", "spouse of"))
    
    memory_graph.visualize("step6_memory_rediscovery.html")
    print("Graph updated - Photo triggers rediscovery of forgotten memories")
    time.sleep(1)
    
    # Step 7: Graph after continued use
    print("\nStep 7: After multiple recall sessions, memory network strengthens")
    # Strengthen well-practiced memories
    memory_graph.strengthen_node_and_connections("paris_trip", 2.0)
    memory_graph.strengthen_node_and_connections("lisa", 1.5)
    memory_graph.strengthen_node_and_connections("eiffel_tower", 1.2)
    memory_graph.strengthen_node_and_connections("john", 1.0)
    
    # Add anniversary memory
    anniversary = MemoryNode("anniversary", "25th Anniversary", "event", "general_event", 0.8)
    memory_graph.add_node(anniversary)
    memory_graph.add_connection(MemoryConnection("paris_trip", "anniversary", "celebrated"))
    memory_graph.add_connection(MemoryConnection("lisa", "anniversary", "celebrated with"))
    memory_graph.add_connection(MemoryConnection("john", "anniversary", "celebrated with"))
    
    memory_graph.visualize("step7_strengthened_network.html")
    print("Final graph shows strengthened memory network with new connections")
    
    return memory_graph

# Run the demo if this script is executed directly
if __name__ == "__main__":
    memory_graph = run_memory_bridge_demo()
    
    print("\nDemo complete! Memory Bridge AI has created a dynamic graph visualization.")
    print("Open the HTML files to see how the memory graph evolved at each step.")