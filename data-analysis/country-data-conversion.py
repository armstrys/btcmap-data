import os
import json

# Set the working directory to the script's directory
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# Specify the input directory containing the GeoJSON files
input_directory_path = 'geojson-regions-10m'

# Specify the output directory where you want to save the JSON files
output_directory_path = 'country-area-outputs'

# Function to extract elements from a GeoJSON feature
def extract_elements(feature):
    # Convert "id" to lowercase
    id_lower = feature["properties"].get("iso_a2", "").lower()
    
    extracted_feature = {
        "id": id_lower,
        "tags": {
            "type": "country",
            "iso_a2": feature["properties"].get("iso_a2", ""),
            "iso_a3": feature["properties"].get("iso_a3", ""),
            "wikidataid": feature["properties"].get("wikidataid", ""),
            "name": feature["properties"].get("formal_en", ""),
            "type": feature["properties"].get("type", ""),
            "sovereignt": feature["properties"].get("sovereignt", ""),
            "continent": feature["properties"].get("continent", ""),
            "region_un": feature["properties"].get("region_un", ""),
            "subregion": feature["properties"].get("subregion", ""),
            "region_wb": feature["properties"].get("region_wb", ""),
            "region_un": feature["properties"].get("region_un", ""),
            "lat": feature["properties"].get("label_y", ""),
            "lon": feature["properties"].get("label_x", ""),
            "population": feature["properties"].get("pop_est", ""),
            "population:rank": feature["properties"].get("pop_rank", ""),
            "population:year": feature["properties"].get("pop_year", ""),
            "gdp_md": feature["properties"].get("gdp_md", ""),
            "gdp_year": feature["properties"].get("gdp_year", ""),
            "economy": feature["properties"].get("economy", ""),
            "income_grp": feature["properties"].get("income_grp", ""),
            "geo_json": feature["geometry"]
        }
    }
    
    return extracted_feature

# Iterate through files in the directory
for filename in os.listdir(input_directory_path):
    if filename.endswith(".geojson"):
        file_path = os.path.join(input_directory_path, filename)
        
        # Load the GeoJSON file
        with open(file_path, 'r') as file:
            geojson_data = json.load(file)
        
        # Check if "features" key exists in the GeoJSON data
        if "features" in geojson_data:
            # Process each feature in the GeoJSON data
            for feature in geojson_data['features']:
                extracted_feature = extract_elements(feature)
                id_lower = extracted_feature["id"]
                
                # Create an output filename in the format id.json
                output_filename = f"{id_lower}.json"
                
                # Write the extracted feature to a separate JSON file
                output_file_path = os.path.join(output_directory_path, output_filename)
                with open(output_file_path, 'w') as output_file:
                    json.dump(extracted_feature, output_file, indent=2)
        else:
            # If there is no "features" key, assume the entire file is a single feature
            extracted_feature = extract_elements(geojson_data)
            id_lower = extracted_feature["id"]
            
            # Create an output filename in the format id.json
            output_filename = f"{id_lower}.json"
            
           # Write the extracted feature to a separate JSON file in the output directory
            output_file_path = os.path.join(output_directory_path, output_filename)
            with open(output_file_path, 'w') as output_file:
                json.dump(extracted_feature, output_file, indent=2)

print("Separate JSON files created in the specified output directory.")