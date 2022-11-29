# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 19:10:00 2022

@author: Abdullah Azhar
"""

## This File combines the Traffic Flows Data and the Travel Times Data and merges them for Modelling

from Libraries import *
from Extracting_JSON_Dumps_V2 import JSON_processing,Travel_Times_Traffic_Flows
from Traffic_Flows_Study_Manipulation import extracting_files,DF_Preparation,DF_Manipulation,analyzing_counts,average_times


# %%
####### TRAVEL TIMES

#Folder_JSONs = 'JSON Responses'
# Folder_JSONs1 = "Test Times Faisal"
# Folder_JSONs = "Test Times Tollinton"
Folder_JSONs = "JSON Responses for Flows"
#Folder_JSONs = 'JSON Responses for Flows/H_to_B'
Master_Dict1 = {}
Master_Dict = {}

#Folder_JSONs = 'J'


Master_Dict = JSON_processing(Folder_JSONs,Master_Dict=Master_Dict)

Keys_Times = Master_Dict.keys()
print(f"Travel Times from the following junctions have been extracted: \n\n {list(Keys_Times)}")

DF = pd.DataFrame(Master_Dict['Tollinton'])

out = Travel_Times_Traffic_Flows(DF)


# %%
##### TRAFFIC FLOWS

#savepath = "PSCA 2018.pkl"
#savepath = "PSCA Avari and Faisal Chowk.pkl"
savepath = "PSCA Amalagamated Data.pkl"

#directory_name = "Testing Directory"
#savepath = "Testing_Pipeline_path_6-Jun.csv"

#DF = extracting_files(directory_name,savepath=savepath)
#DF = DF_Preparation(savepath)
#Locations = DF['Location'].unique()

DF_Amalgamated = pd.read_csv("PSCA Amalagamated Data Preprocessed.csv")
print(f"Traffic Flows for the following junctions have been extracted: \n\n {DF_Amalgamated['Location'].unique()}")

DF_Amalgamated = DF_Amalgamated.loc[(DF_Amalgamated['Location']=='Bashir Sons') | (DF_Amalgamated['Location']=='Tollinton Market')]

#origin_dir='Faisal Chowk ( Assembly Hall)'
#destination_dir = 'Avari Hotel(TS)'

#Counts,Master_Merged = DF_Manipulation(DF,origin_dir="Avari Hotel(TS)",destination_dir="Faisal ")
Counts, Master_Merged = DF_Manipulation(DF_Amalgamated,direction=True,destination_dir="Bashir Sons",origin_dir="Tollinton Market")
#Counts,Master_Merged = pd.read_csv("Faisal to Avari Counts All.csv"),pd.read_csv("Faisal to Avari Merged ALL.csv")



# Counts['date'] = pd.to_datetime(Counts['date'])
# Counts['Day of Week'] = Counts['date'].dt.dayofweek
# Counts['Date_modified'] = Counts['date'].dt.month.astype(str)+"-"+Counts['date'].dt.day.astype(str)

#Counts,Master_Merged = pd.read_csv("Counts H to B (E-W) 7-Jun.csv"),pd.read_csv("Counts Merged H to B (E-W) 7-Jun.csv")
Time_Bucket_Indexing = pd.read_csv("Time Buckets Indexing.csv")
Average_Times = average_times(Master_Merged,out,Time_Bucket_Indexing)

Average_Times.to_csv("Comparing Highcourt-Bashir Times.csv",index=False)

Average_Times = pd.read_csv("Comparing Bashir-to-Tollinton Times.csv")
Average_Times1 = Average_Times[['Time Bucket','Time Difference','Duration_Traffic (s)']]
Average_Times1 = Average_Times1.set_index(['Time Bucket'],drop=True)
Average_Times1 = Average_Times1.rename(columns={'Time Difference':'Safe City Travel Times','Duration_Traffic (s)':'Google API Travel Times'})
cols = [v for v in list(Average_Times1.columns)]
import plotly.express as px
fig = px.line(Average_Times1, x=Average_Times1.index, y=cols)
fig.write_html("Bashir Sons-Tollinton Intersection.html")

# New_DF = pd.merge(Counts,out,how='inner',left_on=['Date_modified','time bucket'],right_on=['Date_modified','time bucket'])






