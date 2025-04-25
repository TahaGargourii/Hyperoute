#!/usr/bin/env python3
import sys
import osmnx as ox
import networkx as nx


def build_weighted_graph(graphml_path):
    print("📥 Loading scored graph...")
    G = ox.load_graphml(graphml_path)
    print(f"✅ Graph loaded with {len(G.nodes)} nodes and {len(G.edges)} edges")
    print("🔧 Adding 'weight' attribute to each edge...")
    eps = 1e-3  # prevent division by zero
    for u, v, k, data in G.edges(keys=True, data=True):
        q = data.get("quality_score")
        try:
            q = float(q) if q is not None else 0.0
        except ValueError:
            q = 0.0
        data["weight"] = 1.0 / (q + eps)
    return G


def route(G, orig_point, dest_point):
    print("🔍 Finding nearest nodes...")
    orig_node = ox.get_nearest_node(G, orig_point, method="euclidean")
    dest_node = ox.get_nearest_node(G, dest_point, method="euclidean")
    print(f"🗺 Routing from node {orig_node} to {dest_node}...")

    path = nx.shortest_path(G, orig_node, dest_node, weight="weight")
    print(f"✅ Path has {len(path)} nodes")

    coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in path]
    return path, coords


def main():
    if len(sys.argv) != 6:
        print("Usage: python etl/route.py <graphml> <orig_lat> <orig_lon> <dest_lat> <dest_lon>")
        sys.exit(1)

    graphml_path = sys.argv[1]
    orig_lat = float(sys.argv[2]); orig_lon = float(sys.argv[3])
    dest_lat = float(sys.argv[4]); dest_lon = float(sys.argv[5])

    G = build_weighted_graph(graphml_path)
    path, coords = route(G, (orig_lat, orig_lon), (dest_lat, dest_lon))

    print("\n🛣️ Route coordinates:")
    for lat, lon in coords:
        print(f"{lat:.6f}, {lon:.6f}")

if __name__ == "__main__":
    main()
