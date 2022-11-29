# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file to play around with databases in pandas 

"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import statistics 
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
from pyproj import CRS
import contextily as ctx



dirname = os.path.dirname(__file__)
print(dirname)

ind_times = "Database_Schools_Paths.csv"
total_times = "Database_Schools_Trajecs.csv"

ind_df = pd.read_csv(ind_times)
ind_df.set_index(ind_df['Timestamp'])

total_df = pd.read_csv(total_times)
total_df.set_index(total_df['Timestamp'])


days = total_df['Day'].unique()
dayslots = total_df['Dayslot'].unique()
timeslots = total_df['Timeslot'].unique()

mean_mins_weekdays = total_df.loc[total_df['Dayslot']=='Weekdays']['Duration_Traffic (mins)'].mean()
mean_mins_weekends = total_df.loc[total_df['Dayslot']=='Weekend']['Duration_Traffic (mins)'].mean()
mean_mins_mondays = total_df.loc[total_df['Dayslot']=='Monday']['Duration_Traffic (mins)'].mean()


mean_mins_tuesdays = total_df.loc[total_df['Day']=='Tuesday']['Duration_Traffic (mins)'].mean()

mean_timeslots = {}

for i in timeslots:
    mean_timeslots[i] = total_df.loc[total_df['Timeslot']==i]['Duration_Traffic (mins)'].mean()

mean_dayslots = {}

for j in dayslots:
    mean_dayslots[j] = total_df.loc[total_df['Dayslot']==j]['Duration_Traffic (mins)'].mean()
    
days_mean = {}

for k in days:
    days_mean[k] = total_df.loc[total_df['Day']==k]['Duration_Traffic (mins)'].mean()

    
by_distance = total_df.sort_values(by='Distance (m)',ascending=False)



## Segregating the Data Frame into different groups based on journeyID
journeys_grouped = total_df.groupby(['Journey_ID'])
journey_0 = journeys_grouped.get_group(0)

total_journeys = len(journeys_grouped) 
filtered_df = pd.DataFrame()

for i in range(total_journeys):
    journeyid = journeys_grouped.get_group(i)
    unique_distances = journeyid['Distance (m)'].unique()
    journeyid['distance_filter'] = ((journeyid['Distance (m)']-unique_distances.mean())/unique_distances.std())
    x = journeyid.loc[(journeyid['distance_filter']<1.5) & (journeyid['distance_filter']>-1.5)]
    filtered_df = filtered_df.append(x)
    print(f"Appending Journey: {i}")
    

journeys_filtered_grouped = filtered_df.groupby(['Journey_ID'])

geometries_journeys = gpd.GeoSeries.from_wkt(filtered_df['Trajectory_Linestring'])
geometries_segments = gpd.GeoSeries.from_wkt(ind_df['Trajectory_Linestring'])

gpd_journeys = gpd.GeoDataFrame(filtered_df,geometry=geometries_journeys,crs="EPSG:4326")
gpd_segments = gpd.GeoDataFrame(ind_df,geometry=geometries_segments,crs="EPSG:4326")

gpd_journeys_webmercator = gpd_journeys.to_crs(epsg=3857)
gpd_segments_webmercator = gpd_segments.to_crs(epsg=3857)


grouping_segments_days = gpd_segments_webmercator.groupby(['Date'])
keys = grouping_segments_days.groups.keys() #returns a dictionary of unique keys

last = grouping_segments_days.get_group('2022-01-10')

fig, ax = plt.subplots(figsize=(14,10))
last.plot(ax=ax,
          column='Normalized CI',
          cmap='Spectral',
          scheme='quantiles',
          k=5,
          legend=True,
          legend_kwds={'title': 'Normalized Congestion Index'})



ax.get_legend().set_title("CongestionIndex")
ax.get_legend().set_bbox_to_anchor((1.5,1))

ctx.add_basemap(ax=ax)

plt.savefig('Testing.png',dpi=300)

