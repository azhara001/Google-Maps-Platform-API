# -*- coding: utf-8 -*-
"""
Created on Thu May 12 14:51:16 2022

@author: Abdullah Azhar

Pending Tasks:
    Explore formats other than pickle to optimize data reading and writing from csv files
    
"""

## This script file takes the PSCA Datasets and the Travel Times Dataset and prepares it for Modeling 

from Libraries import *
pd.set_option('display.max_columns',None)


def extracting_files(PSCA_Path="",savepath=""):
    Folders = os.listdir(PSCA_Path)
    Master_DataFrame = pd.DataFrame()
    Master_Dict = {}
    F = len(Folders)

    for i,folder in enumerate(Folders):
        print(f"Executing Folder: {folder}")
        path = os.path.join(PSCA_Path,folder)
        Folders_2 = os.listdir(os.path.join(PSCA_Path,folder))
        Master_Dict[folder] = Folders_2
        
        for n,file in enumerate(Folders_2):
            path1 = os.path.join(path,file)
            path2 = os.listdir(path1)
            Master_Dict[folder][n] = {file:path2}
            L = len(path2)
            for i,xls in enumerate(path2):
                to_read = os.path.join(path1,xls)
                try:
                    df = pd.read_excel(to_read,header=1)
                except:
                    continue
                df = df.drop(labels=['Checkpoint','Lane','Speed','Picture URL'],axis=1)
                Master_DataFrame = Master_DataFrame.append(df)
    Master_DataFrame.to_pickle(savepath)
    return Master_DataFrame

def DF_Preparation(path="PSCA 2018 Data.pkl",direction=False):
    DF = pd.read_pickle(path)
    DF['Passing Time'] = pd.to_datetime(DF['Passing Time'],infer_datetime_format=True)
    DF['Date'] = DF['Passing Time'].dt.date.astype(str)
    DF['Month'] = DF['Passing Time'].dt.month
    DF['Time'] = DF['Passing Time'].dt.time
    DF = DF.set_index('Passing Time')
    
    #Making 15 Minute Buckets for the DataSet
    
    def time_bucket(Time):
        
        Hour = Time.hour
        Minute = Time.minute
        if Minute >= 0 and Minute < 15:
            output = f"{Hour}:00:00 to {Hour}:15:00"
        elif Minute >=15 and Minute < 30:
            output = f"{Hour}:15:00 to {Hour}:30:00"
        elif Minute >=30 and Minute < 45:
            output = f"{Hour}:30:00 to {Hour}:45:00"
        else: 
            if Hour < 23:
                output = f"{Hour}:45:00 to {Hour+1}:00:00"
            else: 
                output = f"{Hour}:45:00 to 00:00:00"
        return output 
        
    
    DF['Time Bucket'] = DF['Time'].apply(time_bucket)
    
    def Parsing_Direction(Direction_Name):
        
        Direction = Direction_Name[len(Direction_Name)-6:len(Direction_Name)]
        return Direction
    
    DF['Direction'] = DF['Direction Name'].apply(Parsing_Direction)
    DF = DF.drop(labels=['Direction Name'],axis=1)
    print(f"The following locations have been extracted : {DF['Location'].unique}")
    path = path.split(".")
    DF.to_pickle(path[0]+' Preprocessed.pkl')
    
    return DF

def DF_Manipulation(DF,direction=False,origin_dir='',destination_dir=''):
    """
    Parameters
    ----------
    DF : TYPE DATAFRAME
        THE DATAFRAME OF PSCA DATA FOR FEATURE EXTRACTION
    direction : BOOL, optional
        DESCRIPTION. The default is False which will calculate directions from West (Upper Mall) to East (Airport) by default.

    Returns
    -------
    DF : TYPE DATAFRAME
        MANIPULATED DATAFRAME FOR PSCA DATA.
    """
    Master_Dict = {}
    Master_Counts,Master_Merged = pd.DataFrame(),pd.DataFrame()
    dest, origin, alphabeta, intersection,date,timebucket = [],[],[],[],[],[]
    
    Unlicensed,Licensed = DF.loc[DF['Vehicle Plate'] == 'Unlicensed'], DF.loc[DF['Vehicle Plate'] != 'Unlicensed']
    
    print(f"Unlicensed Entries: {len(Unlicensed)} out of {len(DF)}")
    print(f"Remaining Licensed Entries: {len(Licensed)}. Percentage: {(len(Licensed)/len(DF))*100} %")
    DF = Licensed
        
    Locations = DF['Location'].unique()
    Counts = DF.groupby(['Location','Date','Time Bucket'])['Vehicle Plate'].count()
    
    print(f"This Dataset contains the following junctions: {Locations}")

    if direction == True:
        Destination = DF.loc[DF['Direction']=='E to W']
    else:
        Destination = DF.loc[DF['Direction']=='W to E']
    
        ## APPROACH 1 
    Origin = DF.loc[DF['Location']==origin_dir].groupby(['Date','Time Bucket'])
    Destination = DF.loc[DF['Location']==destination_dir].groupby(['Date','Time Bucket'])
    
    
    Keys = list(Destination.groups.keys())
    
    for iteration,key in enumerate(Keys):
        print(key)
        try:
            d1 = Destination.get_group(key)
            o1 = Origin.get_group(key)
            o_total = o1
            
            # if iteration > 1:
            #     o_previous = Origin.get_group(Keys[iteration-1])
            # else:
            #     o_previous = o1
                
            # o_total = o1.append(o_previous)
            
            dest.append(d1.shape[0]) #number of vehicles in destination camera appended
            count_d = d1.shape[0] #number of vehicles in destination 
            
            merged = d1.merge(o_total,on='Vehicle Plate',how='outer')
            merged_filtered = merged.dropna(subset=(['Location_x','Location_y']))
            gamma = merged_filtered.shape[0]
            intersection.append(gamma)
            origin.append(o1.shape[0])
            date.append(key[0])
            timebucket.append(key[1])
            
            Master_Merged = Master_Merged.append(merged)
            
            print(f'Iteration: {iteration}/{len(Keys)}')
            print(f"Intersection Vehicles: {gamma}")
        except KeyError:
            print("No Dates Found in either and/or origin and destination")
            continue
            
    DataFrame_Final = pd.DataFrame({'date':date,'time bucket':timebucket,'Origin Count':origin,'Destination_Count':dest,'Intersection Count':intersection})
    
    return DataFrame_Final, Master_Merged

def analyzing_counts(DF=pd.DataFrame(),direction="W to E"):
    Test = DF.loc[DF['Direction']==direction]
    Test = Test.loc[Test['Vehicle Plate']!='Unlicensed']
    Pivot_B = pd.pivot_table(Test,values='Vehicle Plate',index='Date',columns='Location',aggfunc='count')
    return Pivot_B

def average_times(DF=pd.DataFrame(),DF_Times=pd.DataFrame(),Time_Indexing=pd.DataFrame()):
    DF = DF.dropna(axis=0,how='any')
    DF['Timestamp_y'] = pd.to_datetime(DF['Date_y'] +" "+ DF['Time_y'])
    DF['Timestamp_x'] = pd.to_datetime(DF['Date_x'] +" "+ DF['Time_x'])
    DF['Time Difference'] = (DF['Timestamp_x']-DF['Timestamp_y']).dt.total_seconds()
    DF=DF[DF['Time Difference']>=0]
    DF_Grouped = DF.groupby(['Time Bucket_x'])['Time Difference'].mean()
    
    
    Duration = list(DF_Times['Duration_Traffic (s)','0'])
    Time_Bucket = list(DF_Times['time bucket'])
    DF_Times = pd.DataFrame({"time bucket":Time_Bucket,'Duration_Traffic (s)':Duration})
    
    DF_Times_Grouped = DF_Times.groupby(['time bucket'])['Duration_Traffic (s)'].mean()
    
    Merged = pd.concat([DF_Grouped,DF_Times_Grouped],axis=1)
    
    Merged = Merged.dropna(axis=0,how='any')
    Merged['Time Bucket'] = Merged.index
    Indexed_Average_Times = Merged.set_index(['Time Bucket'],drop=True)
    Indexed_Average_Times = pd.merge(Merged,Time_Indexing,on='Time Bucket',how='inner')
    print(Indexed_Average_Times.columns)
    Indexed_Average_Times = Indexed_Average_Times.sort_values(by=['Index'],ascending=True)
    
    # Indexed_Average_Times = Indexed_Average_Times.index(['Index'],drop=False)

    
    
    return Indexed_Average_Times
    
    
    
    
     
    
    




