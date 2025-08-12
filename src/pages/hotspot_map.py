import streamlit as st
import json
import requests
import folium
from streamlit_folium import st_folium

# Load metal data from JSON
with open("C:/Users/Bhoomi/Sparkathon/predictive-demand-analytics-main/src/metal_data.json", "r") as f:
    metal_data = json.load(f)

# Get selected metal
metal = st.session_state.get("selected_metal", "aluminum").lower()

# Filter data for selected metal and end-of-life = 2025
matches = [
    item for item in metal_data
    if item["metal"].lower() == metal and item["sale_year"] + item["warranty_years"] == 2025
]

# Count locations
location_counts = {}
for item in matches:
    loc = item["location"]
    location_counts[loc] = location_counts.get(loc, 0) + 1

# Geocode locations using OpenStreetMap Nominatim
hotspots = []
for loc, count in location_counts.items():
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={loc}"
    try:
        res = requests.get(url, headers={"User-Agent": "streamlit-app"})
        geo = res.json()
        if geo:
            hotspots.append({
                "location": loc,
                "count": count,
                "lat": float(geo[0]["lat"]),
                "lon": float(geo[0]["lon"])
            })
    except Exception as e:
        st.error(f"Geocoding failed for {loc}: {e}")

# Display map
if hotspots:
    st.title(f"{metal.capitalize()} Hotspots (EOL = 2025)")

    map_center = [hotspots[0]["lat"], hotspots[0]["lon"]]
    fmap = folium.Map(location=map_center, zoom_start=5)

    for h in hotspots:
        folium.CircleMarker(
            location=[h["lat"], h["lon"]],
            radius=h["count"] * 4,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.7,
            popup=f"{h['location']} ({h['count']})"
        ).add_to(fmap)

    st_folium(fmap, width=700, height=500)
else:
    st.warning("No hotspots found for this metal with end-of-life in 2025.")
