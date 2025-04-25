import folium

# Paste in the route coordinates you just got:
route_coords = [
    (51.519611, -0.106227),
    (51.519653, -0.106244),
    (51.519825, -0.106348),
    # … all the way to the last point …
    (51.520134, -0.107248),
]

def main():
    # 1️⃣ Center the map on the start point
    m = folium.Map(location=route_coords[0], zoom_start=16)

    # 2️⃣ Draw the route polyline
    folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

    # 3️⃣ Mark start and end
    folium.Marker(route_coords[0], tooltip="Start").add_to(m)
    folium.Marker(route_coords[-1], tooltip="End").add_to(m)

    # 4️⃣ Save to HTML
    m.save("route.html")
    print("🖼️ Route map saved to route.html")

if __name__ == "__main__":
    main()
