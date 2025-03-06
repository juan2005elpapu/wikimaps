
import folium 
import webview
import os

# Create a map centered at a location (latitude, longitude)
latitude, longitude = 4.7110, -74.0721  # Bogotá, Colombia
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Add a marker
folium.Marker(
    [latitude, longitude],
    popup="Bogotá, Colombia",
    tooltip="Click for more info"
).add_to(m)

# Save the map as an HTML file
map_path = "map.html"
m.save(map_path)

# Open it in a PyWebView window
webview.create_window("Interactive Map", os.path.abspath(map_path))
webview.start()
