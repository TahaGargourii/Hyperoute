import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry

def main():
    # Load the GeoJSON file
    print("📂 Loading GeoJSON...")
    gdf = gpd.read_file("etl/central_london_bumps.geojson")

    print("✅ Loaded GeoJSON!")
    print(f"Number of bumps: {len(gdf)}")
    print(f"Columns available: {gdf.columns}")
    print(f"\nSample row:\n{gdf.iloc[0]}")

    # Connect to Postgres
    print("🔌 Connecting to database...")
    engine = create_engine("postgresql://hyperuser:hyperpass@localhost:5432/hyperroute")

    # Show some info before upload
    print("⬆️ Uploading to PostGIS...")
    print("🔍 Preview of GeoDataFrame:")
    print(gdf.head())
    print("\n🧭 CRS (Coordinate Reference System):", gdf.crs)
    print("📐 Geometry Type:", gdf.geometry.geom_type.unique())

    # Upload to PostGIS with correct geometry type
    gdf.to_postgis(
        name="traffic_bumps",
        con=engine,
        if_exists="replace",
        index=False,
        dtype={"geometry": Geometry("LINESTRING", srid=4326)}
    )

    print("✅ Upload complete!")

if __name__ == "__main__":
    main()
