import json
import pandas as pd
from pyproj import Transformer
import os


# Load GeoJSON file
with open("we_transfer.geojson", "r", encoding="utf-8") as f:
    data = json.load(f)

# Prepare coordinate transformer: EPSG:2056 (CH1903+ / LV95) → EPSG:4326 (WGS84)
transformer = Transformer.from_crs("EPSG:2056", "EPSG:4326", always_xy=True)

# Extract and convert
records = []
for feature in data["features"]:
    props = feature["properties"]
    coords = feature["geometry"]["coordinates"]
    
    address = f'{props.get("TEXTE", "").strip()} {props.get("NUMERO_MAI", "").strip()}'
    lon, lat = transformer.transform(coords[0], coords[1])  # x, y → lon, lat
    
    records.append({
        "address": address,
        "latitude": lat,
        "longitude": lon
    })

# Create DataFrame
df = pd.DataFrame(records)

# Preview
print(df.head())

# Optional: save to CSV
df.to_csv("lausanne_addresses.csv", index=False)
