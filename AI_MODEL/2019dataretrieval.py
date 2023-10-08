import pandas as pd
#get only data for 2019
df = pd.read_csv("fire_archive_M-C61_337361.csv")

df['year'] = df['acq_date'].str[:4].astype(int)

filtered_df = df[df['year'] == 2019]

filtered_df = filtered_df.drop(columns=['year'])

#%%
#only keep fire with confidence higher than 30

filtered_df = filtered_df[(filtered_df['confidence'] > 40)]

#%%

filtered_df = filtered_df[['longitude', 'latitude', 'acq_date']]

filtered_df.to_csv("datawithoutdem.csv", index=False)
