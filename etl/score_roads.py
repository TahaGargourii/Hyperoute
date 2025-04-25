import osmnx as ox
import networkx as nx
from multiprocessing import Pool, cpu_count


def compute_score(edge_data):
    score = 0
    available = 0

    highway = edge_data.get("highway")
    if highway:
        available += 1
        if highway == "motorway": score += 5
        elif highway == "primary": score += 4
        elif highway == "residential": score += 3
        else: score += 2

    surface = edge_data.get("surface")
    if surface:
        available += 1
        if surface == "asphalt": score += 3
        elif surface == "paved": score += 2
        elif surface == "gravel": score -= 2
        elif surface == "unpaved": score -= 3

    lit = edge_data.get("lit")
    if lit == "yes":
        available += 1
        score += 1

    # Avoid division by zero
    if available == 0:
        return None
    return score / available


def score_edge(args):
    u, v, k, data = args
    score = compute_score(data)
    return (u, v, k, score)


def main():
    print("🚀 Starting score_roads.py script...")
    print("📥 Loading graph from GraphML...")
    G = ox.load_graphml("data/greater-london-roads.graphml")

    print(f"✅ Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")
    print("⚙️ Scoring edges in parallel using", cpu_count(), "cores...")

    # Prepare edge list for parallel processing
    edge_list = [(u, v, k, data) for u, v, k, data in G.edges(keys=True, data=True)]

    with Pool(cpu_count()) as pool:
        results = pool.map(score_edge, edge_list)

    # Assign quality_score back to the graph
    for u, v, k, score in results:
        G[u][v][k]["quality_score"] = score if score is not None else -1

    print("💾 Saving scored graph to data/greater-london-roads-scored.graphml...")
    ox.save_graphml(G, filepath="data/greater-london-roads-scored.graphml")
    print("✅ Done! Scored graph saved.")

if __name__ == "__main__":
    main()
