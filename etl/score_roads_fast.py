# etl/score_roads_fast.py

from pyrosm import OSM
import geopandas as gpd
from sqlalchemy import create_engine

def main():
    print("📦 Loading drivable road edges from PBF...")
    osm = OSM("data/greater-london.osm.pbf")
    # nodes=False returns only the edges table; no retain_all/infrastructure flags needed
    edges = osm.get_network(network_type="driving", nodes=False)
    print(f"✅ Retrieved {len(edges)} road segments")

    # 2️⃣ Define vectorized scoring maps
    highway_map = {
        "motorway": 5, "trunk": 4, "primary": 4,
        "secondary": 3, "tertiary": 2, "residential": 1
    }
    surface_map = {
        "asphalt": 3, "paved": 2,
        "cobblestone": -1, "gravel": -2, "unpaved": -3
    }

    # lit: yes=1, everything else=0
    edges["lit_score"] = (edges["lit"] == "yes").astype(int)

    # 3️⃣ Compute vectorized scores
    edges["high_score"] = edges["highway"].map(highway_map).fillna(1)
    edges["surface_score"] = edges["surface"].map(surface_map).fillna(0)
    # count non-null components per row
    edges["n_comp"] = edges[["high_score", "surface_score", "lit_score"]].notnull().sum(axis=1)
    edges["sum_score"] = edges["high_score"] + edges["surface_score"] + edges["lit_score"]
    # avoid division by zero
    edges["quality_score"] = edges["sum_score"] / edges["n_comp"].replace(0, 1)

    # 4️⃣ Write to PostGIS
    print("💾 Writing scores to PostGIS table `road_quality`...")
    engine = create_engine("postgresql://hyperuser:hyperpass@localhost:5432/hyperroute")
    edges[["geometry", "quality_score"]].to_postgis(
        "road_quality", engine, if_exists="replace", index=False
    )
    print("✅ Done! Table `road_quality` created.")

if __name__ == "__main__":
    main()
