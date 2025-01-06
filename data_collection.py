import ee
import requests
import os
import pandas as pd

# Initialize Google Earth Engine
def initialize_gee():
    ee.Initialize()

# Download satellite imagery using Google Earth Engine
def download_satellite_imagery(output_folder, roi_coordinates, start_date, end_date):
    roi = ee.Geometry.Polygon(roi_coordinates)
    dataset = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterBounds(roi) \
        .filterDate(start_date, end_date) \
        .sort('CLOUDY_PIXEL_PERCENTAGE') \
        .first()

    task = ee.batch.Export.image.toDrive(
        image=dataset,
        description='Sentinel2_Imagery',
        folder=output_folder,
        scale=10,
        region=roi.getInfo()['coordinates'],
        fileFormat='GeoTIFF'
    )
    task.start()
    print("Exporting satellite image to Google Drive...")

# Fetch public datasets via API
def download_public_dataset(api_url, params, output_file):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Data saved as '{output_file}'")
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Main function to run the data collection
def collect_data():
    # Create output folder
    output_folder = "raw_data"
    os.makedirs(output_folder, exist_ok=True)

    # Satellite imagery collection
    initialize_gee()
    roi_coordinates = [[30.0, -1.0], [30.0, 1.0], [32.0, 1.0], [32.0, -1.0], [30.0, -1.0]]
    download_satellite_imagery(output_folder, roi_coordinates, '2023-01-01', '2023-12-31')

    # Public dataset collection (e.g., rainfall)
    api_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "parameters": "PRECTOT",
        "community": "AG",
        "longitude": 30.0,
        "latitude": -1.0,
        "start": "20230101",
        "end": "20231231",
        "format": "CSV"
    }
    download_public_dataset(api_url, params, f"{output_folder}/rainfall_data.csv")

if __name__ == "__main__":
    collect_data()
