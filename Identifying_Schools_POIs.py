# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 12:25:36 2022

@author: Abdullah Azhar
"""

## Using Google Places API, Finding School Clusters around our major commerical hubs

from Google_API import Google_API
import pandas as pd
import geopandas as gpd
import json
import time

commercial_centroids = 'Centroids_Commerical.csv'
ucs = 'Master File_Union Councils.csv'


df_commercial = pd.read_csv(commercial_centroids)
df_ucs = pd.read_csv(ucs)

access = Google_API()

testing = df_commercial.loc[0]
testing_lat= testing['Latitude']
testing_lng = testing['Longitude']

m_t_lat = [31.480013]
m_t_lng = [74.323722]

ucs_lat = list(df_commercial['Latitude'])
ucs_lng = list(df_commercial['Longitude'])


# output = access.nearbysearch(placetype='School',lat=testing_lat,lng=testing_lng,radius=3000,keyword='school')

# output_json = json.dumps(output)

# with open('Schools_Search',"w") as file_saved:
#     file_saved.write(output_json)

# ucs_lat = list(df_ucs['latitude'])
# ucs_lng = list(df_ucs['longitude'])

# print(len(ucs_lat) == len(ucs_lng))

def extract_API(latitude='',longitude=''):
    master_schools = []
    for i in range(len(latitude)):
        
        output = access.nearbysearch(placetype='school',lat=latitude[i],lng=longitude[i],radius=200,keyword='school')
        master_schools.extend(output)    
        print(f'point {i} of {len(latitude)}')
        #time.sleep(5)
        if i == 5:
            time.sleep(2)
    schools_df = pd.DataFrame(master_schools)    
    #master_schools_unique = schools_df.drop_duplicates() 
    return schools_df
    
#output = extract_API(latitude=ucs_lat, longitude=ucs_lng)
#output.to_csv('commercial_hubs2.csv',index=False)
# output = access.nearbysearch(placetype='school',lat='31.465387',lng='74.418376',radius=500,keyword='school')   

path_schools = 'unique_Schools_API.csv'
df_schools = pd.read_csv(path_schools)
geometry = gpd.points_from_xy(df_schools['lng'], df_schools['lat'],crs='EPSG:4326')
gdf_schools = gpd.GeoDataFrame(df_schools,geometry=geometry)
gdf_schools = gdf_schools.to_crs('EPSG:3857')
gdf_schools.to_csv('Schools API Unique Reprojected.csv',index=False)





