# etl/extract_roads.py
from pyrosm import OSM
import osmnx as ox

def main():
    # 1️⃣ Initialize Pyrosm with your PBF
    print("📦 Reading OSM PBF for driving network...")
    osm = OSM("data/greater-london.osm.pbf")

    # 2️⃣ Extract nodes & edges for driving
    nodes, edges = osm.get_network(
        nodes=True,              # return nodes GeoDataFrame
        network_type="driving"   # only drivable highways
    )
    print(f"✅ Retrieved {len(nodes)} nodes and {len(edges)} edges")

    # 3️⃣ Build a NetworkX MultiDiGraph
    print("🔗 Converting to NetworkX graph...")
    G_drive = osm.to_graph(
        nodes, edges,
        graph_type="networkx"    # get a NetworkX MultiDiGraph
    )
    print(f"✅ Graph has {len(G_drive.nodes)} nodes and {len(G_drive.edges)} edges")

    # 4️⃣ Save to GraphML for downstream routing
    output = "data/greater-london-roads.graphml"
    ox.save_graphml(G_drive, output)
    print(f"💾 Saved graph to {output}")

if __name__ == "__main__":
    main()
