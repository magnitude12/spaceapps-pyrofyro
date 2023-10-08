#integrating from the climate data csvs
import pandas as pd

df = pd.read_csv("datawithoutclimate.csv")
df1 = pd.read_csv("lstdataoutput.csv")
df2 = pd.read_csv("chirp1.csv")
df3 = pd.read_csv("chirps7output.csv")
df4 = pd.read_csv("atdata2019.csv")
df['lst'] = df1['Scaled_LST']
df['prcp'] = df2['Precipitation_CHIRPS']
df['7dayprecip'] = df3['Sum_Precipitation_Last_7_Days_CHIRPS']
df['at'] = df4['2_at']

#%%
#getting K temperature in °C
df['lst'] = df['lst'] * 0.02
df['lst'] = df['lst'] - 273.15
df['at'] = df['at'] -273.15


df.to_csv("prepared_data.csv", index=False)