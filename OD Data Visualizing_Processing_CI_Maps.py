# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 07:31:23 2022

@author: Abdullah Azhar

Data Manipulation and Analysis of the Master Database File (csv)
"""

# -*- coding: utf-8 -*-

from Libraries import *
print('All Libraries Imported')


#Reading the Database from csv and converting it into Pandas DataFrame
### Reading Files and converting them into Pandas DataFrame

def read_file(path=""):
    df = pd.read_csv(path)
    df.set_index(df['Timestamp_QGIS'])
    return df

path = "Master Database Compiled 12-Apr-22.csv"
#path = "Database_Schools_Paths.csv"
#path = "Database Total Journey Times School Closure Analysis.csv"
total_df_original = read_file(path)
total_df_original['Timestamp'] = pd.to_datetime(total_df_original['Timestamp_QGIS'])
original = total_df_original


# Filtering only the required timeslots
T_slots_total = list(total_df_original['Timeslot'].unique())

T_slots = ['07:30 - 8:00 hours','08:00 - 8:30 hours','08:30 - 9:00 hours','09:00 - 9:30 hours','9:30 - 10:00 hours','12:30 - 13:00 hours','13:00 - 13:30 hours','13:30 - 14:00 hours','14:00 - 14:30 hours','14:30 - 15:00 hours','15:00 - 15:30 hours','17:00 - 17:30 hours','17:30 - 18:00 hours','18:00 - 18:30 hours','18:30 - 19:00 hours','19:30 - 20:00 hours','20:00 - 20:30 hours']

Removed_slots = set(T_slots_total) - set(T_slots)

for x in Removed_slots:
    total_df_original = total_df_original.loc[total_df_original['Timeslot']!=x]
    

# Calculating Velocity (km/h) for total journeys
total_df_original['velocity (km/h)'] = total_df_original['Distance (km)']/(total_df_original['Duration_Traffic (mins)']/60)
original = total_df_original


# Dividing data into multiple holiday slots
winter_break_start = '2021-12-23'
winter_break_end = '2022-01-06'
covid_50_percent = '2022-01-21'
normal_slot = '2022-02-14'
spring_break_start = '2022-03-15'
spring_break_end = '2022-03-28'
post_spring_break = '2022-04-02'
ramadan_start = '2022-04-03'

def holidays_slots(date):
    if date < winter_break_start:
        holidayslot = '1. Before Winter Break'
        slot_index = 1
    elif date >= winter_break_start and date <= winter_break_end:
        holidayslot = '2. During Winter Break'
        slot_index = 2
    elif date > winter_break_end and date < covid_50_percent:
        holidayslot = '3. After Winter Break'
        slot_index = 3
    elif date >= covid_50_percent and date < normal_slot:
        holidayslot = '4. Capacity Reduced to 50%'
        slot_index = 4
    elif date >= normal_slot and date < spring_break_start:
        holidayslot = '5. Normal Activity Before Spring Break'
        slot_index = 5
    elif date >= spring_break_start and date <= spring_break_end:
        holidayslot = '6. Spring Break'
        slot_index = 6
    elif date > spring_break_end and date < ramadan_start:
        holidayslot = '7. Post Spring Break'
        slot_index = 7
    elif date >= ramadan_start:
        holidayslot = '8. Ramadan'
        slot_index = 8
    else:
        print('Erroneous Holiday Slot Detected')
    return holidayslot

total_df_original['Holiday_Slot']= total_df_original['Date'].apply(holidays_slots)
original = total_df_original 


## Dividing Data with respect to morning/afternoon/evening slots
def creating_peakslots(timeslot):
    
    if timeslot == '07:30 - 8:00 hours' or timeslot == '08:00 - 8:30 hours' or timeslot == '08:30 - 9:00 hours' or timeslot == '09:00 - 9:30 hours' or timeslot == '09:30 - 10:00 hours':
        peakslot = 'Morning'
    elif timeslot == '12:30 - 13:00 hours' or timeslot == '13:00 - 13:30 hours' or timeslot == '13:30 - 14:00 hours' or timeslot == '14:00 - 14:30 hours' or timeslot =='14:30 - 15:00 hours' or timeslot == '15:00 - 15:30 hours':
        peakslot = 'Afternoon'
    elif timeslot == '17:00 - 17:30 hours' or timeslot == '17:30 - 18:00 hours' or timeslot == '18:00 - 18:30 hours' or timeslot == '18:30 - 19:00 hours' or timeslot == '19:30 - 20:00 hours' or timeslot == '20:00 - 20:30 hours':
        peakslot = 'Evening'
    else:
        peakslot = 'NA'
    return peakslot
        
total_df_original['Peakslot'] = total_df_original['Timeslot'].apply(creating_peakslots)


## Analysis with Tuesdays and other weekdays
def mondays(day):
    
    if day == 'Monday':
        x = '1. Monday'
    elif day == 'Saturday':
        x = '2. Saturday'
    elif day == 'Sunday':
        x = '0. Sunday'
    elif day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday':
        x = '3. Weekday'
    return x

total_df_original['Dayslot'] = total_df_original['Day'].apply(mondays)
    

def tuesdays(day):
    
    if day == 'Tuesday':
        dayslot = '1. Tuesday'
    elif day == 'Saturday':
        dayslot = '2. Saturday'
    elif day == 'Sunday':
        dayslot = '0. Sunday'
    elif day == 'Monday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday':
        dayslot = '3. Weekday'
    return dayslot
    
total_df_original['DaySlot_Tuesdays'] = total_df_original['Day'].apply(tuesdays)

def wednesdays(day):
    
    if day == 'Wednesday':
        dayslot = '1. Wednesday'
    elif day == 'Saturday':
        dayslot = '2. Saturday'
    elif day == 'Sunday':
        dayslot = '0. Sunday'
    elif day == 'Monday' or day == 'Tuesday' or day == 'Thursday' or day == 'Friday':
        dayslot = '3. Weekday'
    return dayslot

total_df_original['DaySlot_Wednesday'] = total_df_original['Day'].apply(wednesdays)

def thursdays(day):
    
    if day == 'Thursday':
        dayslot = '1. Thursday'
    elif day == 'Saturday':
        dayslot = '2. Saturday'
    elif day == 'Sunday':
        dayslot = '0. Sunday'
    elif day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Friday':
        dayslot = '3. Weekday'
    return dayslot

total_df_original['DaySlot_Thursday'] = total_df_original['Day'].apply(thursdays)

def fridays(day):
    
    if day == 'Friday':
        dayslot = '1. Friday'
    elif day == 'Saturday':
        dayslot = '2. Saturday'
    elif day == 'Sunday':
        dayslot = '0. Sunday'
    elif day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday':
        dayslot = '3. Weekday'
    return dayslot

total_df_original['DaySlot_Friday'] = total_df_original['Day'].apply(fridays)


def saturdays_sundays(day):
    
    if day == 'Saturday':
        dayslot = '1. Saturday'
    elif day == 'Saturday':
        dayslot = '1. Saturday'
    elif day == 'Sunday':
        dayslot = '0. Sunday'
    elif day == 'Monday' or day == 'Tuesday' or day == 'Wednesday' or day == 'Thursday' or day == 'Friday':
        dayslot = '2. Weekday'
    return dayslot

total_df_original['DaySlot_Saturdays_Sundays'] = total_df_original['Day'].apply(saturdays_sundays)

print("Pandas DataFrame converted!")


## Data cleaning of journeywise Data (Dr. Zubair's Idea: 21-Jan-22)
## Removing travel times values that are greater than mean+3*std and less than mean-3*std

# Creating a copy of original dataframe
total_df = total_df_original

# Grouping Data with respect to Journeys
jids = total_df.groupby('Journey_ID')

keys_jids = jids.groups.keys()
filtered_total_df = pd.DataFrame()
removed_total_df = pd.DataFrame()


for key in keys_jids:
    journey = jids.get_group(key)
    mean_time = journey['velocity (km/h)'].mean()
    std = journey['velocity (km/h)'].std()    
    journey_filt = journey.loc[(journey['velocity (km/h)'] > mean_time-3*std) & (journey['velocity (km/h)'] < mean_time+3*std)]
    journey_removed = journey.loc[(journey['velocity (km/h)'] <= mean_time-3*std) | (journey['velocity (km/h)'] >= mean_time+3*std)]
    print(journey_removed.shape)
    filtered_total_df = filtered_total_df.append(journey_filt,ignore_index=True)
    removed_total_df = removed_total_df.append(journey_removed,ignore_index=True)


rows_removed = total_df.shape[0] - filtered_total_df.shape[0]
print(f"Total Journeys DataFrame Filtered. Total no. of rows deleted: {rows_removed}")


# plt.hist(filtered_total_df['Duration (s)'],bins=50)
# plt.hist(total_df['Duration (s)'],bins=50)


# j0 = gps1.get_group(0)
# j0f = gps.get_group(0)

#plt.hist(j0['Duration (s)'],bins=50,align='mid')
#plt.hist(j0f['Duration (s)'],bins=50)


# %%
# Plotting Variations in Monday Velocities (on a city level) for mornings

mornings_mondays = filtered_total_df.loc[(filtered_total_df['Peakslot']=='Morning') & (filtered_total_df['Day']=='Monday')]
entries = mornings_mondays.shape[0]

dates_groups = mornings_mondays.groupby('Date')
keys = dates_groups.groups.keys()

date = []
avg_velocity = []


for i,key in enumerate(keys):
    print(i,key)
    dateslot = dates_groups.get_group(key)
    peaks = dateslot.groupby('Timeslot')
    pkey = peaks.groups.keys()
    
    means = []
    for j,p_key in enumerate(pkey):
        print(p_key)
        avg_vel = peaks.get_group(p_key)['velocity (km/h)'].mean()
        means.append(avg_vel)
        print(avg_vel)
        
        
    date.append(key)
    avg_velocity.append(sum(means)/len(means))
    

# %%
#Calculating Percentage Changes wrt Sunday per slot 


H_slot = filtered_total_df.groupby('Holiday_Slot')
H_keys = H_slot.groups.keys()
total = pd.DataFrame()
master_list = []

#Average_percentage_Sundays
for hkey in H_keys:
    
    group = H_slot.get_group(hkey)
    journeys = group.groupby('Journey_ID')
    J_keys = journeys.groups.keys()
    
    for jkey in J_keys:
        
        H_J_slot = journeys.get_group(jkey)
        
        Hour_group = H_J_slot.groupby('Timeslot')
        Time_keys = Hour_group.groups.keys()
        
        for tkey in Time_keys:
            slot = Hour_group.get_group(tkey)
            print(Time_df)
            df = slot
            sunday_avg = slot.loc[slot['Day'] == 'Sunday']['velocity (km/h)'].mean()
            
            def percentages(velocity):
                percentage_diff = ((velocity-sunday_avg)/sunday_avg)*-100
                return percentage_diff
            
            def percentage_difference(perc_monday,perc_weekdays):
                diff = ((perc_monday-perc_weekdays)/perc_weekdays)*100
                return diff
                
            slot['Percentages Sundays'] = slot['velocity (km/h)'].apply(percentages)
            
            total = total.append(slot,ignore_index=True)
        print(f"Journey_ID: {jkey} percentages calculated")
        
    print(f"Holiday Slot: {hkey} percentages calculated")
    
# %%
            
def means_percentages(df):
    
    df = df.loc[df['Peakslot']=='Morning']
    df = df.loc[df['Dayslot']=='3. Weekday']
    js = df.groupby('Journey_ID')
    keys = js.groups.keys()
    
    journey_id = []
    weekdays = []
    vel_means = []
    origins = []
    destinations = []
    trajectory = []
    distance = []
    duration_live = []
    
    for key in keys:
        journey_id.append(key)
        data = js.get_group(key)
        print("I was here")
        value = data['Percentages Sundays'].mean()
        vel = data['velocity (km/h)'].mean()
        origins.append(data['Origin'].unique()[0])
        destinations.append(data['Destination'].unique()[0])
        distance.append(data['Distance (km)'].mean())
        duration_live.append(data['Duration_Traffic (mins)'].mean())
        
        weekdays.append(value)
        vel_means.append(vel)
        trajectory.append(data['Trajectory_Linestring'].unique()[0])
        
    df_weekdays = pd.DataFrame({'Journey_ID':journey_id, 'Origin':origins,'Destination':destinations,'Distance (km)':distance, 'Duration_Live (mins)':duration_live,'Percentages_Weekdays':weekdays,'Velocity Means': vel_means,'Trajectory':trajectory})
    df_weekdays = df_weekdays.sort_values(by='Percentages_Weekdays',ascending=False)
    
    
    return df_weekdays

before_break_weekdays = means_percentages(total.loc[total['Holiday_Slot']=='1. Before Winter Break'])
top_before_weekdays = before_break_weekdays.head(20)
top_before_weekdays.to_csv('Most congested Before Winter Normalized.csv',index=False)
bottom_before_weekdays = before_break_weekdays.tail(20)   
bottom_before_weekdays.to_csv('Least congested Before Winter Normalized.csv',index=False)     


for_velocities = before_break_weekdays.sort_values(by='Velocity Means',ascending=False)
top_before_vels = for_velocities.head(20)
top_before_vels.to_csv('Highest velocities before winter break.csv',index=False)
bottom_before_vels = for_velocities.tail(20)
bottom_before_vels.to_csv('Lowest velocities before winter break.csv',index=False)



ramadan = means_percentages(total.loc[total['Holiday_Slot']=='8. Ramadan'])
top_ramadan = ramadan.head(20)
top_ramadan.to_csv('Most congested Ramadan.csv',index=False)
bottom_ramadan = ramadan.tail(20)
bottom_ramadan.to_csv('Least congested Ramadan.csv',index=False)


for_velocities = ramadan.sort_values(by='Velocity Means',ascending=False)
top_before_vels = for_velocities.head(20)
top_before_vels.to_csv('Highest velocities Ramadan.csv',index=False)
bottom_before_vels = for_velocities.tail(20)
bottom_before_vels.to_csv('Lowest velocities Ramadan.csv',index=False)

    

# %%    


sns.violinplot(x=mornings_mondays['Date'],y=mornings_mondays['velocity (km/h)'])
fig, ax = plt.subplots(figsize=(14,10))
sns.violinplot(x=mornings_mondays['Date'],y=mornings_mondays['velocity (km/h)'],ax=ax)
plt.xticks(rotation=90)
plt.plot(date,avg_velocity)
plt.xticks(rotation=90)
plt.savefig('tesing.png',dpi=500)



# %%
from Libraries import *


monday_mornings_averages = pd.DataFrame()
fig = px.line(mornings_mondays,x='Date',y='velocity (km/h)',title='Monday Morning Velocity Variations',color='Journey_ID')
fig.show()
fig.write_html('testing.html')
















# %%
## Static Congestion Map Calculations on Individual Segments

## Calculating means of velocities for each Journey by grouping DataFrame with respect to journeys and calculating means

j_id_CI = ind_df.groupby('Journey_ID')
normalized_ind_df = pd.DataFrame()

static_congestion_master = pd.DataFrame()
static_list = []

for i in j_id_CI.groups.keys():
    segments_s_keys = j_id_CI.get_group(i).groupby('Journey_Pathway_Tracking')
    
    for j in segments_s_keys.groups.keys():
        
        segments = segments_s_keys.get_group(j)
        staticdict = {}
        
        check_df = segments
        mean_vel = check_df['Velocity (m/s)'].mean()
        std_vel = check_df['Velocity (m/s)'].std()
        check_df['CI Normalized SegmentWise'] = (check_df['Velocity (m/s)']-mean_vel)/std_vel
        normalized_ind_df = normalized_ind_df.append(check_df,ignore_index=True)
        
        index = check_df.index[0]
        historical_average = check_df['Velocity (m/s)'].mean()
        staticdict['Journey_ID'] = i
        staticdict['Segment_ID'] = j
        staticdict['Historical Velocity Average (m/s)'] = historical_average
        staticdict['Trajectory'] = check_df.at[index,'Trajectory_Linestring']
        static_list.append(staticdict)
      
print(f"Journey_ID: {i}")
static_pd = pd.DataFrame(static_list)
static_pd['Historical Velocity Average (km/h)'] = static_pd['Historical Velocity Average (m/s)']*(3600/1000)
geometry_static = gpd.GeoSeries.from_wkt(static_pd['Trajectory'])
gpd_static = gpd.GeoDataFrame(static_pd,geometry=geometry_static,crs='EPSG:4326')
gpd_static = gpd_static.to_crs(epsg=3857)

credits = 'Static Congestion Map for Lahore using Google Directions API'
fig, ax = plt.subplots(figsize=(14,10))
p = gpd_static.plot(ax=ax,
                      column='Historical Velocity Average (km/h)',
                      cmap='gist_rainbow',
                      alpha=0.5,
                      scheme='quantiles',
                      k=8,
                      legend=True,
                      legend_kwds={'title': 'Static Velocities (km/h)'}
                      )

p.axes.get_xaxis().set_visible(False)
p.axes.get_yaxis().set_visible(False)
ax.get_legend().set_bbox_to_anchor((1.5,1))
ctx.add_basemap(ax=ax, source=ctx.providers.OpenStreetMap.Mapnik, attribution=credits)


plt.savefig('Static Congestions.png',dpi=500)

gpd_static = gpd_static.to_crs(epsg=32643) #if reprojecting to QGIS



# %%
j03 = total_df.loc[total_df['Journey_ID'] == 3]
plt.hist(j03['velocity (km/h)'],bins=50,label='Histogram PDF of velocities (km/h')
plt.xlabel('velocities (km/h)')
plt.savefig('testinghist.png', dpi=400)

# %%
j03_f = filtered_total_df.loc[filtered_total_df['Journey_ID'] == 3]
plt.hist(j03_f['velocity (km/h)'],bins=50)
plt.xlabel('Filtered velocities (km/h)')
plt.savefig('filtered.png')

# %%
pivot_removed = pd.pivot_table(removed_total_df,index='Journey_ID',aggfunc='count')
pivot_removed = pivot_removed.sort_values(by='velocity (km/h)',ascending=False)

j91 = total_df.loc[total_df['Journey_ID'] == 91]
plt.hist(j91['velocity (km/h)'],bins=50,label='Histogram PDF of velocities (km/h)',range=(12,28))
plt.xlabel('velocities (km/h)')
plt.savefig('testinghist.png', dpi=400)

# %%
j91_f = filtered_total_df.loc[filtered_total_df['Journey_ID'] == 91]
plt.hist(j91_f['velocity (km/h)'],bins=50,range=(12,28))
plt.xlabel('Filtered velocities (km/h)')
plt.savefig('filtered.png')

# %%
j135 = total_df.loc[total_df['Journey_ID'] == 135]
plt.hist(j135['velocity (km/h)'],bins=50,label='Histogram PDF of velocities (km/h)',range=(17,33))
plt.xlabel('velocities (km/h)')
plt.savefig('testinghist.png', dpi=400)

# %%
j135_f = filtered_total_df.loc[filtered_total_df['Journey_ID'] == 135]
plt.hist(j135_f['velocity (km/h)'],bins=50,range=(17,33))
plt.xlabel('Filtered velocities (km/h)')
plt.savefig('filtered.png')

# %%
j189 = total_df.loc[total_df['Journey_ID'] == 189]
plt.hist(j189['velocity (km/h)'],bins=50,label='Histogram PDF of velocities (km/h)')
plt.xlabel('velocities (km/h)')
plt.savefig('testinghist.png', dpi=400)

# %%
j189_f = filtered_total_df.loc[filtered_total_df['Journey_ID'] == 189]
plt.hist(j189_f['velocity (km/h)'],bins=50)
plt.xlabel('Filtered velocities (km/h)')
plt.savefig('filtered.png')
# %%

js = total_df.groupby('Journey_ID')

kjs = js.groups.keys()

counts = []

for c in kjs:
    number = js.get_group(c)['Journey_ID'].describe()['count']
    counts.append(number)
    
avg = sum(counts)/len(counts)





# %%

## 17-Jan Working on total journeys (Dr. Tahir) 
path = "Means_Workings/"

def means_calculations(df,path,filtered=False):
    divided = df.groupby('Journey_ID')
    journeys = divided.groups.keys()
    
    j_id = []
    mean_velocities = []
    mean_velocity_morning = []
    mean_velocity_afternoon = []
    mean_velocity_evenings = []
    mean_velocity_night = []
    
    journey = []
    peaks = []
    
    for i in journeys:
        a = divided.get_group(i)
        
        mean_velocity = a['velocity (km/h)'].mean()
        j_id.append(i)
        mean_velocities.append(mean_velocity)
        
        mornings = a.loc[a['Peakslot']=='Morning']
        m_mean = mornings['velocity (km/h)'].mean()
        mean_velocity_morning.append(m_mean)
    
        afternoons = a.loc[a['Peakslot']=='Afternoon']
        a_mean = afternoons['velocity (km/h)'].mean()
        mean_velocity_afternoon.append(a_mean)
    
        evenings = a.loc[a['Peakslot']=='Evening']
        e_mean = evenings['velocity (km/h)'].mean()
        mean_velocity_evenings.append(e_mean)
        
        nights = a.loc[a['Peakslot']=='Night']
        n_mean = nights['velocity (km/h)'].mean()
        mean_velocity_night.append(n_mean)
        
    
    dict_means = {'Journey_ID':j_id, 'Mean Velocities (km/h)': mean_velocities, 'Mean Velocities Morning (km/h)':mean_velocity_morning, 'Mean Velocities Afternoon (km/h)': mean_velocity_afternoon, 'Mean Velocities Evenings (km/h)': mean_velocity_evenings, 'Mean Velocities Night (km/h)': mean_velocity_night}
    df_means = pd.DataFrame(dict_means)
    
    df_means = df_means.sort_values(by=['Mean Velocities (km/h)'])
    
    if len(list(df['Holiday_Slot'].unique())) == 1:
        path_append = list(df['Holiday_Slot'].unique())[0]
    else:
        raise AssertionError('Unique holiday slot not properly segregated')
        
    if filtered == False:
        path_final = path+path_append+'Means.csv'
    else:
        path_final = path+path_append+'Filtered_Means.csv'
        
    df_lowest_journey_id = df_means.index[0]
    df_lowest_vel = df_means.loc[df_lowest_journey_id,'Mean Velocities (km/h)']
    
    df_means.to_csv(path_final,index=False)
    return df_means


## Division into Holiday Slots of Original DataFrame 
bef_wint_break = total_df_original.loc[total_df_original['Holiday_Slot'] == 'Before Winter Break']
means_calculations(bef_wint_break,path=path,filtered=False)
bef_wint_break = sundays_percentages(bef_wint_break,"Percentage_wrt_Sunday_Slot")
#bef_wint_break.to_csv("Before Winter Break.csv",index=False)
pivot_before_wint = pd.pivot_table(bef_wint_break, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
pivot_before_wint_mornings = pd.pivot_table(bef_wint_break.loc[bef_wint_break['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')


# after_wint_break = total_df_original.loc[total_df_original['Holiday_Slot'] == 'After Winter Break']
# means_calculations(after_wint_break,path=path,filtered=False)
# after_wint_break = sundays_percentages(after_wint_break,"Percentage_wrt_Sunday_Slot")
# after_wint_break.to_csv("After Winter Break.csv",index=False)
# pivot_after_wint = pd.pivot_table(after_wint_break, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
# pivot_after_wint_mornings = pd.pivot_table(after_wint_break.loc[after_wint_break['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')

during_wint_break = total_df_original.loc[total_df_original['Holiday_Slot'] == 'During Winter Break']
means_calculations(during_wint_break,path=path,filtered=False)
during_wint_break = sundays_percentages(during_wint_break,"Percentage_wrt_Sunday_Slot")
#during_wint_break.to_csv("During Winter Break.csv",index=False)
pivot_during_wint = pd.pivot_table(during_wint_break, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
pivot_during_wint_mornings = pd.pivot_table(during_wint_break.loc[during_wint_break['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')

## Division into Holiday Slots of Filtered (21-Jan-22 Working) DataFrame 
bef_wint_break_filt = filtered_total_df.loc[filtered_total_df['Holiday_Slot'] == 'Before Winter Break']
means_calculations(bef_wint_break_filt,path=path,filtered=True)
bef_wint_break_filt = sundays_percentages(bef_wint_break_filt,"Percentage_wrt_Sunday_Slot")

bef_wint_break_filt.to_csv("Before Winter Break Filtered.csv",index=False)
pivot_before_wint_filt = pd.pivot_table(bef_wint_break_filt, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
pivot_bef_wint_break_filt_mornings = pd.pivot_table(bef_wint_break_filt.loc[bef_wint_break_filt['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')

# after_wint_break_filt = filtered_total_df.loc[filtered_total_df['Holiday_Slot'] == 'After Winter Break']
# means_calculations(after_wint_break_filt,path=path,filtered=True)
# after_wint_break_filt = sundays_percentages(after_wint_break_filt,"Percentage_wrt_Sunday_Slot")
# after_wint_break_filt.to_csv("After Winter Break Filtered.csv",index=False)
# pivot_after_wint_filt = pd.pivot_table(after_wint_break_filt, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
# pivot_after_wint_break_filt_mornings = pd.pivot_table(after_wint_break_filt.loc[after_wint_break_filt['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')


during_wint_break_filt = filtered_total_df.loc[filtered_total_df['Holiday_Slot'] == 'During Winter Break']
means_calculations(during_wint_break_filt,path=path,filtered=True)
during_wint_break_filt = sundays_percentages(during_wint_break_filt,"Percentage_wrt_Sunday_Slot")
during_wint_break_filt.to_csv("During Winter Break Filtered.csv",index=False)
pivot_during_wint_filt = pd.pivot_table(during_wint_break_filt, values='Percentage_wrt_Sunday_Slot', index=['Peakslot', 'Dayslot'],aggfunc="mean")
pivot_during_wint_break_filt_mornings = pd.pivot_table(during_wint_break_filt.loc[during_wint_break_filt['Peakslot']=='Morning'], values='Percentage_wrt_Sunday_Slot',index=['Timeslot','Dayslot'],aggfunc='mean')

# %%
## Comparing averages on sundays


sundays_v = pd.DataFrame()
sundays_v_filtered = pd.DataFrame()

bef_sunday = bef_wint_break.loc[bef_wint_break['Day'] == 'Sunday']
bef_sunday_filtered = bef_wint_break_filt.loc[bef_wint_break_filt['Day'] == 'Sunday']

during_sunday = during_wint_break.loc[during_wint_break['Day'] == 'Sunday']
during_sunday_filtered = during_wint_break_filt.loc[during_wint_break_filt['Day'] == 'Sunday']

sundays_v = bef_sunday.append(during_sunday)
sundays_v_filtered = bef_sunday_filtered.append(during_sunday_filtered)

pivot_sundays = pd.pivot_table(sundays_v,values='velocity (km/h)',index='Holiday_Slot')
pivot_sundays_filtered = pd.pivot_table(sundays_v_filtered,values='velocity (km/h)',index='Holiday_Slot')




# %%

## Finding the top 5 journeys that have the greatest percentage difference in speeds: weekdays -vs- sundays (for morning slots only!):
    ## An atttempt to identify those journeys most affected by schools (if any)

def means_percentages(df):
    
    df = df.loc[df['Peakslot']=='Morning']
    df = df.loc[df['Dayslot']=='3. Weekday']
    js = df.groupby('Journey_ID')
    keys = js.groups.keys()
    
    journey_id = []
    weekdays = []
    origins = []
    destinations = []
    trajectory = []
    distance = []
    duration_live = []
    
    for key in keys:
        journey_id.append(key)
        data = js.get_group(key)
        print("I was here")
        value = data['Percentage_wrt_Sunday_Slot'].mean()
        origins.append(data['Origin'].unique()[0])
        destinations.append(data['Destination'].unique()[0])
        distance.append(data['Distance (km)'].mean())
        duration_live.append(data['Duration_Traffic (mins)'].mean())
        
        weekdays.append(value)
        trajectory.append(data['Trajectory_Linestring'].unique()[0])
        
    df_weekdays = pd.DataFrame({'Journey_ID':journey_id, 'Origin':origins,'Destination':destinations,'Distance (km)':distance, 'Duration_Live (mins)':duration_live,'Percentages_Weekdays':weekdays,'Trajectory':trajectory})
    df_weekdays = df_weekdays.sort_values(by='Percentages_Weekdays',ascending=False)
    
    
    return df_weekdays

before_break_weekdays = means_percentages(bef_wint_break_filt)
top_before_weekdays = before_break_weekdays.head(11)
top_before_weekdays.to_csv('Most congested.csv',index=False)
bottom_before_weekdays = before_break_weekdays.tail(11)   
bottom_before_weekdays.to_csv('Least congested.csv',index=False)     
during_break_weekdays = means_percentages(during_wint_break_filt)

# %%
top = pd.read_csv("Most congested.csv")
bottom = pd.read_csv("Least congested.csv")

geometry_top = gpd.GeoSeries.from_wkt(top['Trajectory'])
gpd_top = gpd.GeoDataFrame(top,geometry=geometry_top,crs="EPSG:4326")
gpd_top = gpd_top.to_crs(epsg=3857)
gpd_top.to_csv("Most conjested reprojected.csv",index=False)

geometry_bottom = gpd.GeoSeries.from_wkt(bottom['Trajectory'])
gpd_bottom = gpd.GeoDataFrame(bottom,geometry=geometry_bottom,crs="EPSG:4326")
gpd_bottom = gpd_bottom.to_crs(epsg=3857)
gpd_bottom.to_csv("Lease conjested reprojected.csv",index=False)





    

     
# %%    

day_slots = total_df.groupby('Day')

    
keys = day_slots.groups.keys()


means = {}
maxs = {}
mins = {}

for i in keys:
    dff = day_slots.get_group(i)['velocity (km/h)'].describe()
    print(dff)
    #path = f"Day Wise Averages{i}.csv"
    #dff.to_csv(path)
    means[i] = day_slots.get_group(i)['velocity (km/h)'].describe()['mean']
    maxs[i] = day_slots.get_group(i)['velocity (km/h)'].describe()['max']
    mins[i] = day_slots.get_group(i)['velocity (km/h)'].describe()['min']
    
a = pd.DataFrame(means,index=means.keys())




#Residential_Commercial Centroids
# path_centroids = 'Centroids_com_res.csv'
# centroids = pd.read_csv(path_centroids)
# gm = gpd.points_from_xy(centroids.Longitude, centroids.Latitude)
# centroids_gdf = gpd.GeoDataFrame(centroids,geometry=gm,crs='EPSG:4326')
# centroids_gdf = centroids_gdf.to_crs(epsg=3857)

# fig, ax = plt.subplots(figsize=(14,10))
# cen = centroids_gdf.plot(ax=ax, column='Type',cmap='PiYG',alpha=0.5, legend=True,linewidth=10)
# ctx.add_basemap(ax=ax, source=ctx.providers.OpenStreetMap.Mapnik, attribution=credits)
# cen.axes.get_xaxis().set_visible(False)
# cen.axes.get_yaxis().set_visible(False)
# plt.savefig('Res_Com.png',dpi=400)



# %%

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
    

print('APPENDED!')
journeys_filtered_grouped = filtered_df.groupby(['Journey_ID'])

print('Converting to geopandas geometries')
geometries_journeys = gpd.GeoSeries.from_tt(filtered_df['Trajectory_Linestring'])
geometries_segments = gpd.GeoSeries.from_wkt(ind_df['Trajectory_Linestring'])

print('Converting to geopandas GeoDataFrame: ')
gpd_journeys = gpd.GeoDataFrame(filtered_df,geometry=geometries_journeys,crs="EPSG:4326")
gpd_segments = gpd.GeoDataFrame(ind_df,geometry=geometries_segments,crs="EPSG:4326")

print('Geopandas data frame converted!')

gpd_journeys_webmercator = gpd_journeys.to_crs(epsg=3857)
gpd_segments_webmercator = gpd_segments.to_crs(epsg=3857)



grouping_segments_days = gpd_segments_webmercator.groupby(['Date'])
keys = grouping_segments_days.groups.keys() #returns a dictionary of unique keys

last = grouping_segments_days.get_group('2022-01-10')
last_morning = last.loc[last['Timeslot'] == '07:30 - 8:00 hours']
last_evening = last.loc[last['Timeslot'] == '12:30 - 01:00 hours']



### Folium Mapping
# Lahore_latlng = [31.520370,74.358749]

# m = folium.Map(location=Lahore_latlng, zoom_start=10,tiles = 'cartodbpositron')

# geojson = folium.features.GeoJson(last_morning, name= "Directions Pathways Morning")
# geojson1 = folium.features.GeoJson(last_morning, name= "Directions Pathways Afternoon")

# geojson.data.get('features')
# geojson.add_to(m)
# geojson1.add_to(m)

# a = last_morning.reset_index()
# a['Geo-ID'] = a.index
# a = a[['Geo-ID','Congestion Index']]

# ## Heatmap Schools 
# schools_path = 'Schools Lat_Lng.csv'

# schools_df = pd.read_csv(schools_path)
# schools_df = schools_df.loc[schools_df['district'] == 'Lahore']
# geometry_schools = gpd.points_from_xy(schools_df['longitude'], schools_df['latitude'],crs='EPSG:4326')
# gpd_schools = gpd.GeoDataFrame(schools_df,geometry=geometry_schools)
# locations = list(zip(schools_df['latitude'],schools_df['longitude']))


# #Available parameters: HeatMap(data, name=None, min_opacity=0.5, max_zoom=18, max_val=1.0, radius=25, blur=15, gradient=None, overlay=True, control=True, show=True)
# HeatMap(locations,name='Schools Clusters HeatMap').add_to(m)



# folium.Choropleth(
#     geo_data = geojson,
#     name = '2022-01-10',
#     data=a,
#     columns = ['Geo-ID','Normalized CI'],
#     fill_color = 'YlOrRd',
#     key_on = 'feature.id',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     ).add_to(m)

# #legend_name= ('Traffic Congestion Index').add_to(m)
# folium.LayerControl().add_to(m)


# credits = 'Congestion Index Map for Lahore using Google Directions API'
# fig, ax = plt.subplots(figsize=(14,10))
# last.plot(ax=ax,
#           column='Normalized CI',
#           cmap='Spectral',
#           alpha=0.5,
#           scheme='quantiles',
#           k=10,
#           legend=True,
#           legend_kwds={'title': 'Normalized Congestion Index'})


# ax.get_legend().set_title("CongestionIndex")
# ax.get_legend().set_bbox_to_anchor((1.2,1))

# ctx.add_basemap(ax=ax, source=ctx.providers.OpenStreetMap.Mapnik, attribution=credits)

# dir(ctx.providers) #to get a list of providers in ctx 
# ctx.providers.Stamen.TonerLite



# plt.savefig('Testing1.png',dpi=300)

# %%

## Breaking Down Segment Wise Data (ind_df) into timeslots and computing averages and then plotting to show dynamic congestion map for Lahore 
## THIS IDEA HAS BEEN DROPPED FOR NOW (21-Jan-2022)


ind_df['Normalized CI'] = ind_df['Normalized CI']*(-1)
vmin = ind_df['Normalized CI'].describe()['min']
vmax = ind_df['Normalized CI'].describe()['max']
print(vmin)
print(vmax)

timestamp_slot = ind_df.groupby('Timestamp')
keys_timestamps_slots = timestamp_slot.groups.keys()

# To get the keys of the group: 
time_slots_ind = ind_df.groupby('Timeslot')
keys_times_slots = time_slots_ind.groups.keys()
master_dataframe = pd.DataFrame()

for i in keys_times_slots:
    j_id_group = time_slots_ind.get_group(i).groupby('Journey_ID')
    keys_journey_ids = j_id_group.groups.keys()
    print(f'Timeslot: {i}')
    for j in keys_journey_ids:
        segment_group = j_id_group.get_group(j).groupby('Journey_Pathway_Tracking')
        keys_segments_ids = segment_group.groups.keys()
        print(f'journey_id: {j}')
        for seg in keys_segments_ids:
            #print(f'seg: {seg}')
            ind_segment = segment_group.get_group(seg)
            #print(f"ind_segment: {ind_segment}")
            ind_segment = ind_segment.reset_index()
            #print(f'segment_id: {k}')
            means = ind_segment.mean(numeric_only=True)
            means['Timeslot'] = ind_segment.at[0,'Timeslot']
            means['Trajectory_Linestring'] = ind_segment.at[0,'Trajectory_Linestring']
            #means['Journey_Pathway_Tracking'] = ind_segment[]
            master_dataframe = master_dataframe.append(means,ignore_index=True)
    geometry = gpd.GeoSeries.from_wkt(master_dataframe['Trajectory_Linestring'])
    gpd_timeslot = gpd.GeoDataFrame(master_dataframe,geometry=geometry,crs='EPSG:4326')
    gpd_timeslot = gpd_timeslot.to_crs(epsg=3857)

    credits = 'Congestion Index Map for Lahore using Google Directions API'
    fig, ax = plt.subplots(figsize=(14,10))
    p = gpd_timeslot.plot(ax=ax,
                          column='Normalized CI',
                          cmap='YlOrRd',
                          alpha=0.5,
                          scheme='quantiles',
                          k=5,
                          vmin=vmin,
                          vmax= vmax,
                          legend=True,
                          legend_kwds={'title': 'Normalized Congestion Index'}
                          )

    p.axes.get_xaxis().set_visible(False)
    p.axes.get_yaxis().set_visible(False)
    

# %%
    title = f"Time_Slot: {i}"
    ax.get_legend().set_title(title)
    ax.get_legend().set_bbox_to_anchor((1.5,1))
    ctx.add_basemap(ax=ax, source=ctx.providers.OpenStreetMap.Mapnik, attribution=credits)
    
    #dir(ctx.providers) #to get a list of providers in ctx 
    #ctx.providers.Stamen.TonerLite
    splits = i.split(sep=":")
    path = f"Map_TimeSlot {splits[0]+splits[1]+splits[2]}"
    path = f"Map_TimeSlot_ {path}.png"
    
    plt.savefig(path,dpi=300)

# %%

schools_path = 'Schools Lat_Lng.csv'
schools = pd.read_csv(schools_path)
schools = schools.loc[schools['district'] == 'Lahore']

from pyproj import Proj
myProj = Proj('proj=utm zone=43 datum=WGS84 units=m no_defs ellps=WGS84 towgs84=0,0,0') 
schools['utm_x'], schools['utm_y'] = myProj(schools['longitude'].to_list(),schools['latitude'].to_list())
geometry_schools = gpd.points_from_xy(schools['utm_x'], schools['utm_y'])
gpd_schools = gpd.GeoDataFrame(schools,geometry=geometry_schools,crs='EPSG:32643')
gpd_schools = gpd_schools.to_crs('EPSG:3857')


gpd_schools.to_csv('Schools Data reprojected.csv',index=False)

# geometry_schools = gpd.points_from_xy(schools['longitude'],schools['latitude'])
# gpd_schools = gpd.GeoDataFrame(schools,geometry=geometry_schools,crs='EPSG:4326')
# gpd_schools.to_crs(epsg=32643)
# gpd_schools.to_csv('schools data reprojected gpd.csv', index=False)

