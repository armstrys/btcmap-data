import requests
import geopandas as gpd
import os
import numpy as np
import h3pandas
import json  # Import the json module
import matplotlib.pyplot as plt

# Set the working directory to the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# Step 1: Get Latest Merchants from btcmap.org/elements
url = "https://api.btcmap.org/elements"  # Updated URL
response = requests.get(url)

# Check if the response status code indicates success
if response.status_code != 200:
    raise RuntimeError(
        f"Failed to retrieve data. Status code: {response.status_code}"
    )
try:
    # Attempt to decode the JSON response
    data = response.json()
except json.JSONDecodeError:
    raise RuntimeError("Error decoding JSON response.")

# Step 2: Extract Element ID and Position (Lon, Lat)
ids = []
lats = []
lons = []
for item in data:
    osm_json = item['osm_json']
    ids.append(item.get('id'))
    lons.append(osm_json.get('lon'))
    lats.append(osm_json.get('lat'))

# Step 3: build gdf of data
gdf = gpd.GeoDataFrame(
    data={'id': ids, 'lat': lats, 'lon': lons},
    geometry=gpd.points_from_xy(lons, lats),
    crs='EPSG:4326'  # load in google WGS84 lat/lon crs
)
gdf = gdf.dropna(how='any')

if len(gdf) == 0:
    raise RuntimeError("No valid data found in the API response.")

# Step 4: Calculate hexagon-based density as merchants per square kilometer
h3_resolution = 2  # this is not a real unit - 0-15 valid where 0 is coarse
gdf_h3_agg = gdf.h3.geo_to_h3_aggregate(h3_resolution, operation='count')
gdf_h3_agg = gdf_h3_agg[['id', 'geometry']].rename(columns={'id': 'count'})
gdf_h3_agg = gdf_h3_agg.to_crs('EPSG:3857') # convert to web mercator for areas
gdf_h3_agg['density'] = gdf_h3_agg['count'] / (gdf_h3_agg.area)
gdf_h3_agg.plot(column='count')
plt.show()

# Save the density data as a shapefile in the current script directory
shapefile_output = os.path.join(script_directory, 'merchant_density.shp')
gdf_h3_agg.to_file(shapefile_output)
print(f"Merchant density exported as '{shapefile_output}'")
