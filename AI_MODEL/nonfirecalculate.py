import pandas as pd

df = pd.read_csv("datawithdem.csv")
df =df[df['DEM'] <= 4000]

df['fire'] = 1
#%%
#make new data within from the df for non fire values as random points
import random
unique_coordinates = df[['longitude', 'latitude']].drop_duplicates()

date_list = df['acq_date'].unique().tolist()

new_rows = pd.DataFrame(columns=['longitude', 'latitude', 'acq_date', 'DEM', 'fire'])

max_repetitions = 4

target_total_rows = 6000

coordinate_counters = {}

while len(new_rows) < target_total_rows:
    selected_coordinates = unique_coordinates.sample(1)
    longitude = selected_coordinates['longitude'].values[0]
    latitude = selected_coordinates['latitude'].values[0]
    
    if (longitude, latitude) not in coordinate_counters:
        coordinate_counters[(longitude, latitude)] = 1
    elif coordinate_counters[(longitude, latitude)] >= max_repetitions:
        continue
    else:
        coordinate_counters[(longitude, latitude)] += 1

    random_date = random.choice(date_list)
    
    dem_value = df[(df['longitude'] == longitude) & (df['latitude'] == latitude)]['DEM'].values[0]
    
    new_row = pd.DataFrame([[longitude, latitude, random_date, dem_value, 0]], columns=['longitude', 'latitude', 'acq_date', 'DEM', 'fire'])
    new_rows = pd.concat([new_rows, new_row], ignore_index=False)

result_df = pd.concat([df, new_rows], ignore_index=False)

result_df = result_df.sample(target_total_rows, random_state=1)

print(result_df)


result_df.to_csv("datawihtoutclimate.csv", index=False)