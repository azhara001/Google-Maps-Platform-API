from pandas.core.frame import DataFrame
from Google_API import Google_API
#import Extracting_JSON_Dumps
import pandas as pd

from datetime import datetime
import geopandas

print("Beginning Execution ...")


API_Key_Abdullah = "AIzaSyCtxc33UlHmSRg7kXrCBtX1VYEUJU5cwA8"
API_Key_Test = "AIzaSyALsZCmxIKPCO8vJHhNMxxJiEWDkKpo-Qc"


access = Google_API()

######
# For Commerical_vs_Residential Times and Paths

def commercial_vs_residential_times_API(Database_Times_Filepath='',Database_Pathways_Filepath ='',commercial_centroids ='',residential_centroids=''):
    
    date_time = str(datetime.now())
    Current_Time = str(datetime.now())
    Current_Time = Current_Time.split(" ")
    Ping_Date = Current_Time[0]
    Ping_Time = Current_Time[1]
    Ping_Time = Ping_Time.split(":")
    
    print(f"Current Timestamp of API Call: {date_time} ")

    print("Extracting Commercial hubs coordinates")
    commercial_df = pd.read_csv(commercial_centroids)
    commercial_latlng = commercial_df['Latitude,Longitude']

    print("Extracting Residential hubs coordinates")
    residential_df = pd.read_csv(residential_centroids)
    residential_latlng = residential_df['Latitude,Longitude']

    counter_com = 0
    counter_res = 1
    master_list_times = []
    master_list_trajectory = []
    Journey_ID = 0
    
    
    for residential_i in range(len(residential_latlng)):
        print(f"Residential_Counter: {counter_res} ")
        for commercial_j in range(len(commercial_latlng)):
            access.get_directions_API(commercial_latlng[commercial_j],residential_latlng[residential_i],mode="driving",date_time=date_time,Journey_ID=Journey_ID)
            counter_com += 1
            print(f"Commercial_Counter: {counter_com} ")
    
            # for x in API_trajectory:
            #     master_list_trajectory.append(x)
            
            # for y in API_times:
            #     master_list_times.extend(y)
    
            Journey_ID += 1
        counter_res += 1
        
    # Times_DF = pd.DataFrame(master_list_times)
    # Trajectory_DF = pd.DataFrame(master_list_trajectory)
         
    
    # master_dict = {
    #     "Times" : Times_DF,
    #     "Trajectories" : Trajectory_DF
    #     }

    # Times_DF.to_csv(Database_Times_Filepath,header=False,index=False,mode='a') #appends to existing masterdatabase
    # Trajectory_DF.to_csv(Database_Pathways_Filepath,header=False,index=False,mode='a') #appends to existing masterdatabase 
    # Times_DF.to_csv(f'School Closure Analysis Database/Times Result {Ping_Date}_Time_{Ping_Time[0]}_{Ping_Time[1]}.csv',index=False) #creates a new csv file 
    # Trajectory_DF.to_csv(f'School Closure Analysis Database/Paths Result {Ping_Date}_Time_{Ping_Time[0]}_{Ping_Time[1]}.csv',index=False) #creates a new csv file 
    #Trajectory_DF.to_csv("School_Closure_Analysis_Database_Base_Trajectory.csv",index=False)
    
    return None

def CSV_to_Shapefile(path_times="",path_trajectories=""):
    df_times = pd.read_csv(path_times)
    df_trajectories = pd.read_csv(path_trajectories)

    df_times['Origin Geometry'] =  geopandas.GeoSeries.from_wkt(df_times['Origin Geometry'])
    gpd_times = geopandas.GeoDataFrame(df_times,geometry='Origin Geometry')
    gpd_times.to_file("Sample Times_waypoints.shp")

    df_trajectories['Trajectory'] = geopandas.GeoSeries.from_wkt(df_trajectories['Trajectory_Linestring'])
    gpd_trajectories_Linestring = geopandas.GeoDataFrame(df_trajectories,geometry='Trajectory')
    gpd_trajectories_Linestring.to_file("Sample Trajectories_linestring_waypoints.shp")
    return None


Database_Times_Filepath = "School_Closure_Analysis_Database_times.csv"
Database_Pathways_Filepath = "School_Closure_Analysis_Database_trajectory.csv"
Database_Base_Pathways_Filepath = "School_Closure_Analysis_Database_trajectory_Base Trajectories.csv"

Commercial_Centroids_Filepath = "Centroids_Commerical.csv"
Residential_Centroids_Filepath = "Residential_Hubs_Zameen.csv"


output = commercial_vs_residential_times_API(Database_Times_Filepath,Database_Pathways_Filepath,Commercial_Centroids_Filepath,Residential_Centroids_Filepath)




