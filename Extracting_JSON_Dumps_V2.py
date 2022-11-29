# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 12:17:47 2021
Last Modified: 28-Mar-22 15:19:00 2022

@author: Abdullah Azhar
Extracting JSON Dumps and converting them into CSV Test Code 
"""

from Libraries import *
from Extract_JSON_Function import extract_JSON
from save_details import save_details
# from storing_into_DB import save_details


def JSON_processing(Folder_JSONs,Master_Dict={}):
    JSON_Folders = os.listdir(Folder_JSONs)
    print(JSON_Folders)
    

    Total_JSONs =  sum([len(os.listdir(f"{Folder_JSONs}/{x}")) for x in os.listdir(Folder_JSONs)])    
    
    
    for i,folder in enumerate(os.listdir(Folder_JSONs)):
        output = []
        json_pathway = f"{Folder_JSONs}/{folder}"
        json_database = os.listdir(json_pathway)
        json_dicts = {}
             
        output.extend(extract_JSON(json_database, json_pathway,i,Total_JSONs)['paths'])       
        # df_global_list = output1['global master list']
        
        # for each in df_global_list:
        #     journey_list = each.values.tolist()
        #     for journey in journey_list:
        #         print(journey[5])
        #         save_details(journey)
        Master_Dict[folder] = output
        
    #output_df = pd.DataFrame(output)
    # return output_df, Master_Dict
    return Master_Dict

def Travel_Times_Traffic_Flows(DF=pd.DataFrame()): 
    DF = DF.drop(labels=['Origin','Destination','Distance (m)','Distance (km)','Duration (mins)','Mode','date',],axis=1)
    
    output_df = pd.DataFrame()
    DF['Timestamp_QGIS'] = pd.to_datetime(DF['Timestamp_QGIS'])
    DF['Time'] = DF['Timestamp_QGIS'].dt.time
        
    def time_bucket(time):
        Hour = time.hour
        Minute = time.minute
        
        if Minute < 15:
            output = f"{Hour}:00:00 to {Hour}:15:00"
        elif Minute >= 15 and Minute < 30:
            output = f"{Hour}:15:00 to {Hour}:30:00"
        elif Minute >=30 and Minute < 45:
            output = f"{Hour}:30:00 to {Hour}:45:00"
        elif Minute >= 45:
            output = f"{Hour}:45:00 to {Hour+1}:00:00"
        else:
            print('Error')
        return output
    
    DF['time bucket'] = DF['Time'].apply(time_bucket)
    DF_pivot = DF.pivot_table(values=['Duration_Traffic (s)'],columns='Journey_ID',index=['Date','Day','time bucket'],aggfunc='mean')
    DF_pivot = DF_pivot.reset_index()  
    DF_pivot['Date'] = pd.to_datetime(DF_pivot['Date'])
    DF_pivot['Date_modified'] = DF_pivot['Date'].dt.month.astype(str)+"-"+DF_pivot['Date'].dt.day.astype(str)
    # DF_pivot = DF_pivot.stack()
    return DF_pivot





