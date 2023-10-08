import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio
import rioxarray as rxr


dem = rxr.open_rasterio('4326nepal.tif')

dem= dem.rio.reproject("EPSG:4326")


df = pd.read_csv('datawithinforest.csv')
df = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df['longitude'], df['latitude']))

#%%
i = 1
for index, row in df.iterrows():
    latitude = row['geometry'].y
    longitude = row['geometry'].x
    height = dem.sel(x = longitude,y = latitude,method = 'nearest').values[0]
   # print(r[rowIndex, colIndex])
    df.at[index,'DEM'] = height
    print(i)
    i=i+1
    
df = df[['longitude', 'latitude', 'acq_date', 'DEM']]

df.to_csv("datawithdem.csv", index=False)