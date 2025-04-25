#!/usr/bin/env python3
# etl/route_fast.py
# Fast, quality-aware routing using Pyrosm and NetworkX — no GraphML needed

import sys
from pyrosm import OSM
import networkx as nx
import osmnx as ox

# Scoring maps
HIGHWAY_MAP = {
    "motorway": 5, "trunk": 4, "primary": 4,
    "secondary": 3, "tertiary": 2, "residential": 1
}
SURFACE_MAP = {
    "asphalt": 3, "paved": 2,
    "cobblestone": -1, "gravel": -2, "unpaved": -3
}
EPS = 1e-3  # to avoid division by zero


def build_and_score_graph(pbf_path):
    print("📦 Loading drivable network from PBF (Pyrosm)...")
    osm = OSM(pbf_path)
    nodes, edges = osm.get_network(network_type="driving", nodes=True)
    print(f"✅ Got {len(nodes)} nodes and {len(edges)} edges")

    # Vectorized scoring
    print("🔢 Computing quality_score vectorized...")
    edges['lit_score'] = (edges.get('lit', '') == 'yes').astype(int)
    edges['high_score'] = edges['highway'].map(HIGHWAY_MAP).fillna(1)
    edges['surface_score'] = edges['surface'].map(SURFACE_MAP).fillna(0)
    edges['n_comp'] = edges[['high_score','surface_score','lit_score']].notnull().sum(axis=1)
    edges['sum_score'] = edges['high_score'] + edges['surface_score'] + edges['lit_score']
    edges['quality_score'] = edges['sum_score'] / edges['n_comp'].replace(0, 1)

    print("🔧 Converting to NetworkX graph...")
    G = osm.to_graph(nodes, edges, graph_type="networkx")
    print(f"✅ Graph has {len(G.nodes)} nodes and {len(G.edges)} edges")

    print("⚙️ Adding weight=1/(quality_score+eps) to edges...")
    for u, v, key, data in G.edges(keys=True, data=True):
        q = data.get('quality_score', 0) or 0
        data['weight'] = 1.0 / (q + EPS)

    return G


def route(G, orig_point, dest_point):
    print("🔍 Snapping to nearest nodes...")
    orig_node = ox.distance.nearest_nodes(G, X=orig_point[1], Y=orig_point[0])
    dest_node = ox.distance.nearest_nodes(G, X=dest_point[1], Y=dest_point[0])
    print(f"🗺 Routing from {orig_node} to {dest_node}...")

    path = nx.shortest_path(G, orig_node, dest_node, weight='weight')
    print(f"✅ Found path with {len(path)} nodes")
    coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in path]
    return path, coords


def main():
    if len(sys.argv) != 5:
        print('Usage: python etl/route_fast.py <orig_lat> <orig_lon> <dest_lat> <dest_lon>')
        sys.exit(1)

    orig_lat, orig_lon, dest_lat, dest_lon = map(float, sys.argv[1:5])
    G = build_and_score_graph('data/greater-london.osm.pbf')
    _, coords = route(G, (orig_lat, orig_lon), (dest_lat, dest_lon))

    print('\n🛣️ Route coordinates:')
    for lat, lon in coords:
        print(f"{lat:.6f}, {lon:.6f}")

if __name__ == '__main__':
    main()
