import geopandas as gpd
import pandas as pd

shapefile_path = "forest shape/forest.shp"
gdf_shape = gpd.read_file(shapefile_path)

csv_file_path = "datawithoutdem.csv"
df_coords = pd.read_csv(csv_file_path)

gdf_coords = gpd.GeoDataFrame(df_coords, geometry=gpd.points_from_xy(df_coords['longitude'], df_coords['latitude']))

df_coords.crs = "EPSG:4326"

clipped_coords = gpd.sjoin(gdf_coords, gdf_shape, how="inner", op="within")

clipped_coords.to_csv("datawithinforest.csv", index=False)
