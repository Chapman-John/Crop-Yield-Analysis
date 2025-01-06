import pandas as pd
import rasterio

# Load and preview a CSV dataset
def load_csv(file_path):
    df = pd.read_csv(file_path, skiprows=10)  # Adjust skiprows for metadata
    print(f"Loaded dataset from {file_path}:")
    print(df.head())
    return df

# Load and inspect GeoTIFF file
def inspect_geotiff(file_path):
    with rasterio.open(file_path) as src:
        print(f"GeoTIFF file: {file_path}")
        print(f"Width: {src.width}, Height: {src.height}")
        print(f"CRS: {src.crs}")
        print(f"Bounds: {src.bounds}")
        return src

if __name__ == "__main__":
    # Example usage
    rainfall_df = load_csv("raw_data/rainfall_data.csv")
    inspect_geotiff("raw_data/Sentinel2_Imagery.tif")
