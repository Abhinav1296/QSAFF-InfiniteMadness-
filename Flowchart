import matplotlib.pyplot as plt
import networkx as nx

def draw_sci_fi_flowchart():
    G = nx.DiGraph()
    
    # Nodes
    nodes = [
        "User", "Dark Energy Authentication Void", "File Input", "Anti-Matter Encryption Abyss", 
        "Black Hole Multiversal Storage", "Sentient File Chaos Core", "Eternal Swarm & Dark Sentinels", 
        "Chrono-Singularity Recovery Maelstrom", "Output"
    ]
    
    # Edges (Connections between steps)
    edges = [
        ("User", "Dark Energy Authentication Void"),
        ("Dark Energy Authentication Void", "File Input"),
        ("File Input", "Anti-Matter Encryption Abyss"),
        ("Anti-Matter Encryption Abyss", "Black Hole Multiversal Storage"),
        ("Black Hole Multiversal Storage", "Sentient File Chaos Core"),
        ("Sentient File Chaos Core", "Eternal Swarm & Dark Sentinels"),
        ("Eternal Swarm & Dark Sentinels", "Chrono-Singularity Recovery Maelstrom"),
        ("Chrono-Singularity Recovery Maelstrom", "Output"),
        ("Output", "User")
    ]
    
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    # Positioning
    pos = nx.spring_layout(G, seed=42)
    
    # Draw Graph
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color='cyan', edge_color='purple', node_size=3000, font_size=10, font_weight='bold')
    
    plt.title("Sci-Fi Secure File Management Flowchart", fontsize=14, fontweight='bold', color='darkred')
    plt.show()
    
# Run the function
draw_sci_fi_flowchart()
