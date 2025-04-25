import networkx as nx

def main():
    print("📥 Loading graph from GraphML...")
    G = nx.read_graphml("data/greater-london-roads.graphml")

    print(f"✅ Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")
    print("🔍 Sample edge data:")
    u, v = list(G.edges())[0]
    print(G[u][v])

if __name__ == "__main__":
    main()
