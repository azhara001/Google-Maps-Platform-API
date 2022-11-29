import json
from typing import Text
import urllib
import requests
import pandas as pd
import os
from datetime import datetime
import time
import json

class Google_API(object):

    base_url = ''
    path_file = ''
    inputdf = pd.Series(0)
    outputdf = pd.Series(0)
    abs_path = None

    def __init__(self,API_key="",base_url = 'https://maps.googleapis.com/maps/api/'):
        self.API_key = API_key
        self.base_url = base_url

    def get_dir_elements(self):
        """
        This method returns the current working directory of the current file 
        """
        self.abs_path = os.getcwd()
        #self.dir = os.path.dirname(self.abs_path)
        print(os.listdir(self.abs_path))
    
    def extract_places(self,path_file='',asinput = False):
        """
        This function takes a file path as an input and extracts that file path and returns a pandas DataFrame of that file contents
        It can only take a .csv file path or .xlsx file path as an input
 
        """
        if path_file.endswith('.xlsx'):
            try:
                self.inputdf = pd.read_excel(path_file)
            except:
                print(f"\n Error: The file path {self.path_file} does not exist. Use the method: get_dir_elements for a list of the available \n files in your current working directory")
        elif path_file.enswith('.csv'):
            try:
                self.inputdf = pd.read_csv(path_file)
            except:
                print(f"\n Error: The file path {self.path_file} does not exist. Use the method: get_dir_elements for a list of the available \n files in your current working directory")
        else:
            raise Exception("\n Error : The file path to be read is not a .csv or .xlsx filepath. Use the method: get_dir_elements for a list \n of the available files in your current working directory ")

    def get_geocoding(self,input_address=[],reverse_geocoding=False,latlng=''):
        """
        This method is used to convert an input address into a lat_long pair using Google GeoCoding API
        The inputs for this method include:
        the API_code is the url string element that accessess the geocoding API ('geocode' in this case)
        address_input: a list of the input addresses that user wants to extract lat_lng coordinates from 
        
        This method will return a pandas DataFrame 
        """
        if not reverse_geocoding:
            parameters = {'address': input_address, 'key':self.API_key}

            params = urllib.parse.urlencode(parameters)
            url = f"{self.base_url}geocode/json?{params}"
            r = requests.get(url).json()
            print(url)
            if r['status'] == 'OK':
                    lat_lng = r['results'][0]['geometry']['location']
                    lat = str(lat_lng['lat'])
                    lng = str(lat_lng['lng'])
                    lat_lng = f"{lat},{lng}"
                    return lat_lng
            else:
                raise Exception('Data extraction from API was unsuccessful')
        else:
            parameters = {'latlng':latlng,'key':self.API_key}
            params = urllib.parse.urlencode(parameters)
            url = f"{self.base_url}geocode/json?{params}"
            r = requests.get(url).json()
            print(url)
            if r['status'] == 'OK':
                    place_id = r['results'][0]['place_id']
                    return place_id
            else:
                return r['status']
  
    def findplacefromtext(self,API_code,input_address=[]):
        """
        This function uses the Google Places API (Find place from text) to return attributes of the place entered as a text
        This API returns a json file that contains attributes based on the API call
        One can expect Latitude/Longitudes of place entered as a text and/or a unique place_id that can be used in other APIs like Distance Matrix or Directions API
        Fields can include the following: 'business_status,formatted_address,geometry,icon,name,permanently_closed,photo,place_id,plus_code,type'
        This function returns a dictionary of the place entered that contains the following:
        1. Address of place
        2. Name of place
        3. Lat/Lng coordinates
        4. Place id
        """
        parameters = {
            'input': input_address,
            'inputtype' : 'textquery',
            'locationbias' : 'ipbias',
            'fields' : 'formatted_address,geometry,name,permanently_closed,place_id',
            'key' : self.API_key
        }
        params = urllib.parse.urlencode(parameters)
        url = f"{self.base_url}{API_code}/findplacefromtext/json?{params}"
        #print(url)
        r = requests.get(url)
        output_dict = {}
        error_list = []
        
        if r.json()['status'] == 'OK':
            output_dict['user_input'] = input_address
            output_dict['name'] = r.json()['candidates'][0]['name']
            output_dict['address'] = r.json()['candidates'][0]['formatted_address']
            output_dict['place_id'] = r.json()['candidates'][0]['place_id']
            output_dict['lat'] = r.json()['candidates'][0]['geometry']['location']['lat']
            output_dict['lng'] = r.json()['candidates'][0]['geometry']['location']['lng']
            output_dict['status'] = r.json()['status']
            return output_dict
        else:
            print(r.json()['status'])
            output_dict['user_input'] = input_address
            output_dict['status'] = r.json()['status']
            return output_dict

    def get_place_placefromtext(self):
        list_places = []
        print('You were here')

        print(self.inputdf.loc)
        for i,place1 in enumerate(self.inputdf.iloc[:,1]):
            dict = self.findplacefromtext(API_code='place',input_address=place1)
            list_places.append(dict)
            print(i," ", place1)
        return list_places

    def append_to_Excel(self,to_append,content_append=[],path='',sheet_name = ''):
        DF = pd.DataFrame(content_append) #saves the information of the user_input to a pandas DataFrame
        cols = DF.columns

        to_append[DF.columns] = DF[cols]
        to_append.to_excel(path,sheet_name,index=False)

    def nearbysearch(self,placetype='',lat='',lng='',radius=3000):
        """
        For search_nearby API i.e. finds a place in a nearby vicinity specified by latitudes and longitudes (using geocoding API) and specifying a radius (in meters)
        This function uses the Google Places API (nearby_place) to return attributes of the place 
        This API returns a pandas DataFrame that contains attributes based on the API call
        """
        
        parameters = {
        'location' : f"{lat},{lng}",
        'radius' : radius,
        'type': placetype,
        'inputtype' : 'textquery',
        'fields' : 'business_status,formatted_address,geometry,icon,name,permanently_closed,photo,place_id,plus_code,type',
        'key' : self.API_key
        }
        params = urllib.parse.urlencode(parameters)
        url = f"{self.base_url}place/nearbysearch/json?{params}"
        print(url)
        r = requests.get(url).json()
        if r['status'] == 'OK':
            list_return = []
            for i,row in enumerate(r['results']):
                dict = {
                    'name' : r['results'][i]['name'],
                    'lat' : r['results'][i]['geometry']['location']['lat'],
                    'lng' : r['results'][i]['geometry']['location']['lng'],
                    'place_id' : r['results'][i]['place_id'],
                    'place_type' : r['results'][i]['types']
                }
                list_return.append(dict)
            return list_return
        else:
            print(r.json()['status'])
            dict['user_input'] = input_address
            dict['status'] = r.json()['status']
            return dict
        
    def places_getambigious(self,text_input='',lat='',lng='',radius=''):
        """
        For Text Search API i.e. finds a place based on a string with ambigous addresses and responds with a list of places matching the text string and any location bias that has been set
        This function uses the Google Places API (Text Search) to return attributes of the place 
        This API returns a list that contains attributes based on the API call        
        """
        parameters = {
        'query' : text_input,
        'location' : f"{lat},{lng}",
        'radius' : radius,
        'key' : self.API_key 
        }

        params = urllib.parse.urlencode(parameters)
        request_url = f"{self.base_url}place/textsearch/json?{params}"
        r = requests.get(request_url).json()
        output_list = []

        for i,elem in enumerate(r['results']):
            dict = {}
            if r['status'] == 'OK':    
                dict['name'] = r['results'][i]['name']
                dict['formatted_address'] = r['results'][i]['formatted_address']
                dict['lat'] = r['results'][i]['geometry']['location']['lat']
                dict['lng'] = r['results'][i]['geometry']['location']['lng']
            else:
                dict['name'] = text_input, 
                dict['status'] = r['status']            
            output_list.append(dict)   
        return output_list        

    def get_distance_matrix_from_place_id(self,df=pd.Series(0),travel_mode='driving',traffic_model='best_guess',departure_time='now'):
        """
        sample_request = 'https://maps.googleapis.com/maps/api/distancematrix/outputFormat?parameters'
        df = the DataFrame from which the place_ids are to be extracted 
        travel_modes = ['driving','walking','bicycling','transit']
        traffic_model = ['best_guess','pessimistic','optimistic']
        
        """
        filtered_df = df.dropna()
        columns = df.columns 
        bucket_size = 10

        place_ids = list(filtered_df['place_id'])
        place_ids_buckets = [place_ids[i:i + bucket_size] for i in range(0, len(place_ids), bucket_size)]
        place_ids_buckets_formatted = ['|place_id:'.join(elem) for elem in place_ids_buckets]
        output_list = []
        output_dict = {}
        Total_requests = 0
        

        for elem in place_ids_buckets_formatted:
            for bucket_elem in place_ids_buckets_formatted:
                parameters = {
                    'origins' : f"place_id:{elem}",
                    'destinations' : f"place_id:{bucket_elem}",
                    'travel_mode' : travel_mode,
                    'departure_time' : departure_time,
                    'traffic_model' : traffic_model,
                    'key' : self.API_key
                }
                params = urllib.parse.urlencode(parameters)
                url_req = f"{self.base_url}distancematrix/json?{params}"
                r = requests.get(url_req)
                date_time = str(datetime.now())
                date_time_list = date_time.split()
                Total_requests += 1
                json_output = r.json()
                

                for i,origin in enumerate(json_output['origin_addresses']):
                    for j,destination in enumerate(json_output['destination_addresses']):
                        print(f"origin is {origin}")
                        print(f"destination is {destination}")


                        if json_output['rows'][i]['elements'][j]['status'] == 'OK':
                            output_dict = {
                                'source' : origin,
                                'dest' : destination,
                                'kilometers' : json_output['rows'][i]['elements'][j]['distance']['text'],
                                'travel_time' : json_output['rows'][i]['elements'][j]['duration']['text'],
                                'travel_time_in_traffic' : json_output['rows'][i]['elements'][j]['duration_in_traffic']['text'],
                                'date' : date_time_list[0],
                                'time' : date_time_list[1]

                            }
                        else:
                            output_dict = {
                                'source' : origin,
                                'dest' : destination,
                                'kilometers' : 'Not Found',
                                'travel_time' : 'Not Found',
                                'travel_time_in_traffic' : 'Not Found',
                                'date' : date_time_list[0],
                                'time' : date_time_list[1]
                            }
                        output_list.append(output_dict)
        return output_list

    def get_distance_matrix_from_latlng(self,df = pd.Series(0),travel_mode='driving',traffic_model='best_guess',departure_time='now'):
        """
        sample_request = 'https://maps.googleapis.com/maps/api/distancematrix/outputFormat?parameters'
        df = the DataFrame from which the place_ids are to be extracted 
        travel_modes = ['driving','walking','bicycling','transit']
        traffic_model = ['best_guess','pessimistic','optimistic']
        
        """
        filtered_df = df.dropna()
        columns = df.columns 
        bucket_size = 10

        latlng = list(filtered_df['latitude,longitude'])
        latlng_buckets = [latlng[i:i + bucket_size] for i in range(0, len(latlng), bucket_size)]
        latlng_buckets_formatted = ['|'.join(elem) for elem in latlng_buckets]
        output_list = []
        output_dict = {}
        Total_requests = 0
        print('i was here')

        for elem in latlng_buckets_formatted:
            #print(f"elem is {elem}")
            #print(f"type of elem is {type(elem)}")
            elem_list = elem.split('|')
            #print(f"elem converted to list: {elem_list}")
            #print(f"length of elem_list : {len(elem_list)}")
            for bucket_elem in latlng_buckets_formatted:
                bucket_elem_list = bucket_elem.split('|')
                parameters = {
                    'origins' : elem,
                    'destinations' : bucket_elem,
                    'travel_mode' : travel_mode,
                    'departure_time' : departure_time,
                    'traffic_model' : traffic_model,
                    'key' : self.API_key
                }
                params = urllib.parse.urlencode(parameters)
                url_req = f"{self.base_url}distancematrix/json?{params}"
                r = requests.get(url_req)
                date_time = str(datetime.now())
                date_time_list = date_time.split()
                Total_requests += 1
                json_output = r.json()


                for i,origin in enumerate(json_output['origin_addresses']):
                    print(f"The origin latlng is: {elem_list}")
                    for j,destination in enumerate(json_output['destination_addresses']):
                        print(f"The destination latlng is: {bucket_elem_list[j]}")
                        if json_output['rows'][i]['elements'][j]['status'] == 'OK':
                            output_dict = {
                                'source' : origin,
                                'source_latlng' : elem_list[i],
                                'dest' : destination,
                                'dest_latlng' : bucket_elem_list[j],
                                'kilometers' : json_output['rows'][i]['elements'][j]['distance']['text'],
                                'travel_time' : json_output['rows'][i]['elements'][j]['duration']['text'],
                                'travel_time_in_traffic' : json_output['rows'][i]['elements'][j]['duration_in_traffic']['text'],
                                'date' : date_time_list[0],
                                'time' : date_time_list[1]

                            }
                        else:
                            output_dict = {
                                'source' : origin,
                                'source_latlng' : elem_list[i],
                                'dest' : destination,
                                'dest_latlng' : bucket_elem_list[j],
                                'kilometers' : 'Not Found',
                                'travel_time' : 'Not Found',
                                'travel_time_in_traffic' : 'Not Found',
                                'date' : date_time_list[0],
                                'time' : date_time_list[1]
                            }
                        output_list.append(output_dict)
        print(f"The Total number of requests sent for this session are: {Total_requests}")
        return output_list
        time.sleep(30)

    def get_directions_API(self,destination="",origin="",alternatives=True,departure_time='now',mode='walking',date_time="",transit_mode="",Journey_ID = None):
        """
        A Directions API request takes the following form: https://maps.googleapis.com/maps/api/directions/outputFormat?parameters
        
        Parameters:
        alternatives = True/False (if set to True, Directions API will provide more than one route alternative in the response)
        avoid = tolls|highways|ferries|indoor 
        mode = DRIVING,WALKING,BICYCLING,TRANSIT
        traffic_model = best_guess(default)/optimistic/pessimistic
        units = metric (Textual distances are returned using kilometers and meters)
        waypoints = passover or stopover locations may be added 

        """
        Base_Paths_DF = pd.read_csv("School_Closure_Analysis_Database_trajectory_Base Trajectories.csv")
        #print(f"Journey_ID: {Journey_ID}") #for debugging 
        Base_Paths_DF = Base_Paths_DF.loc[lambda df:df['Journey_ID'] == Journey_ID,:]
        Base_Paths_DF_sliced = Base_Paths_DF.dropna(axis=1) #drops those columns that have no value in them 
        #print(f"Base_Paths_DF_sliced {Base_Paths_DF_sliced}") #for debugging 
        Last_column = Base_Paths_DF_sliced.iloc[0,-1:]
        Last_column_str = str(Last_column)
        Last_column_list = Last_column_str.split(" ")
        Last_column_name = Last_column_list[0]
        #print(f"Last_Column: {Last_column_name}") #for debugging 
        Paths = Base_Paths_DF_sliced.loc[:,"step_pathway0":Last_column_name]
        Paths = Paths.values.tolist()[0]
        L_Paths = int(len(list(Paths)))
        Waypoints_List = Paths[0:L_Paths:round(L_Paths/10)]
        

        waypoints = ""

        for point in Waypoints_List:
            point = point[1:len(point)-1]
            points = point.split(",")
            waypoints = waypoints + "via:" + points[1] + "," + points[0] + "|"

        parameters = {
            'origin' : origin,
            'destination' : destination,
            'alternatives' : alternatives,
            'departure_time' : departure_time,
            'mode' : mode,
            'traffic_model': 'best_guess', #you can change this to pessimistic or optimistic as per API docs
            'transit_mode' : transit_mode,
            'units' : 'metric',
            'waypoints' : waypoints,
            'key' : self.API_key
            }
        
        params = urllib.parse.urlencode(parameters)
        url_req = f"{self.base_url}directions/json?{params}"
        #print(url_req) #for debugging
        r = requests.get(url_req)
        r_json = r.json()
        Current_Time = str(datetime.now())
        Current_Time = Current_Time.split(" ")
        Ping_Date = Current_Time[0]
        Ping_Time = Current_Time[1]
        Ping_Time = Ping_Time.split(":")
        Path = f"JSON_Dumps/Json_Dump_{Ping_Date}_Time_{Ping_Time[0]}_{Ping_Time[1]}_Journey_ID{Journey_ID}"
        
        json_object = json.dumps(r_json,indent=4)
        with open(Path,"w") as file_saved:
            file_saved.write(json_object)
        
        number_of_routes = len(r_json['routes'])
        print(f"no. of routes: {number_of_routes}")
        #_________________________________________________________________________________________________________________
        #Code used from stack overflow to decode polylines to lat,lng pairs.
        def decode_polyline(polyline_str):  
            index, lat, lng = 0, 0, 0
            coordinates = []
            changes = {'latitude': 0, 'longitude': 0}

            # Coordinates have variable length when encoded, so just keep
            # track of whether we've hit the end of the string. In each
            # while loop iteration, a single coordinate is decoded.
            while index < len(polyline_str):
                # Gather lat/lon changes, store them in a dictionary to apply them later
                for unit in ['latitude', 'longitude']: 
                    shift, result = 0, 0

                    while True:
                        byte = ord(polyline_str[index]) - 63
                        index+=1
                        result |= (byte & 0x1f) << shift
                        shift += 5
                        if not byte >= 0x20:
                            break

                    if (result & 1):
                        changes[unit] = ~(result >> 1)
                    else:
                        changes[unit] = (result >> 1)

                lat += changes['latitude']
                lng += changes['longitude']

                coordinates.append((lat / 100000.0, lng / 100000.0))
            
            return coordinates
        #_________________________________________________________________________________________________________________        
        
        def Directions_Times(self,r_json):
            
            master_list = [] #To cater to multiple routes (if returned)
            route_counter = len(r_json['routes'])

            for i in range(route_counter): #loop to iterate over the total number of routes returned by the API 
                
                list_steps = []
                Number_of_steps = len(r_json['routes'][i]['legs'][0]['steps']) #calculates the number of total steps as returned by the API
                print(f'No. of steps for executing route: {Number_of_steps}') #prints the number of steps per route

                journey_counter = 1
                for j in range(Number_of_steps):
                    steps_dict = {}
        
                    steps_dict['Journey_ID'] = Journey_ID
                    steps_dict['Route_ID'] = route_counter
                    steps_dict['Journey_Pathway_Tracking'] = journey_counter
                    steps_dict['origin (Lat)'] = f"{r_json['routes'][i]['legs'][0]['steps'][j]['start_location']['lat']}"
                    steps_dict['origin (Lng)'] = f"{r_json['routes'][i]['legs'][0]['steps'][j]['start_location']['lng']}"
                    steps_dict['Origin Geometry'] = f"POINT({steps_dict['origin (Lng)']} {steps_dict['origin (Lat)']})"
                    
                    
                    steps_dict['destination (Lat)'] = f"{r_json['routes'][i]['legs'][0]['steps'][j]['end_location']['lat']}"
                    steps_dict['destination (Lng)'] = f"{r_json['routes'][i]['legs'][0]['steps'][j]['end_location']['lng']}"
                    steps_dict['Destination Geometry'] = f"POINT({steps_dict['destination (Lng)']} {steps_dict['destination (Lat)']})"

                    distance = r_json['routes'][i]['legs'][0]['steps'][j]['distance']['text']
                    blankspace = distance.find(" ")

                    #if distance_unit == 'km':
                    steps_dict['distance'] =  distance[0:blankspace]
                    steps_dict['distance_Unit'] = distance[blankspace+1:len(distance)]
                    
                    duration = r_json['routes'][i]['legs'][0]['steps'][j]['duration']['text']
                    blankspace = duration.find(" ")
                    steps_dict['duration'] =  duration[0:blankspace]
                    steps_dict['duration_Unit'] = duration[blankspace+1:len(duration)]

                    try:
                        duration_in_traffic = r_json['routes'][i]['legs'][0]['steps'][j]['duration_in_traffic']['text']
                        blankspace = duration_in_traffic.find(" ")
                        steps_dict['duration_in_traffic'] =  duration_in_traffic[0:blankspace]
                        steps_dict['duration_in_traffic_unit'] = duration_in_traffic[blankspace+1:len(duration)]
                    except:
                        steps_dict['duration_in_traffic'] = None
                        steps_dict['duration_in_traffic_unit'] = None
                    
                    steps_dict['mode'] =  r_json['routes'][i]['legs'][0]['steps'][j]['travel_mode']
                    steps_dict['date'] = "Time_Stamp: " + date_time
                    #steps_dict['time'] = date_time_list[1]
                    
                    
                    list_steps.append(steps_dict)
                    journey_counter += 1

                route_counter += 1       
            master_list.append(list_steps)
            return master_list

        def Directions_Trajectory(self,r_json,mode=mode):

            master_list = []
            route_counter = len(r_json['routes'])

            for i in range(route_counter): #loop to iterate over the total number of routes returned by the API 
                my_dict_output = {}
                
                my_dict_output['Journey_ID'] = Journey_ID
                my_dict_output['Origin (Lat)'] = r_json['routes'][i]['legs'][0]['start_location']['lat']
                my_dict_output['Origin (Lng)'] = r_json['routes'][i]['legs'][0]['start_location']['lng']
                
                my_dict_output['Destination (Lat)'] = r_json['routes'][i]['legs'][0]['end_location']['lat']
                my_dict_output['Destination (Lng)'] = r_json['routes'][i]['legs'][0]['end_location']['lng']
                
                
                distance = r_json['routes'][i]['legs'][0]['distance']['text']
                blankspace = distance.find(" ")
                my_dict_output['distance'] =  distance[0:blankspace]
                my_dict_output['Distance_Unit'] = distance[blankspace+1:len(distance)]
                    
                duration = r_json['routes'][i]['legs'][0]['duration']['text']
                blankspace = duration.find(" ")
                my_dict_output['duration'] =  duration[0:blankspace]
                my_dict_output['Duration_Unit'] = duration[blankspace+1:len(duration)]

                try:
                    duration_in_traffic = r_json['routes'][i]['legs'][0]['duration_in_traffic']['text']
                    blankspace = duration_in_traffic.find(" ")
                    my_dict_output['Total_duration_traffic'] =  duration_in_traffic[0:blankspace]
                    my_dict_output['Duration_Traffic_Unit'] = duration_in_traffic[blankspace+1:len(duration)]
                    #print("duration_text_i was here")
                except:
                    my_dict_output['Total_duration_traffic'] = None
                    my_dict_output['Duration_Traffic_Unit'] = None
                
                my_dict_output['Mode'] = mode    
                my_dict_output['date'] = "Time_Stamp: " + date_time
                overview_polyline = r_json['routes'][i]['overview_polyline']['points']
                decoded_polyline = decode_polyline(overview_polyline)

                trajectory_multipoint = "MULTIPOINT ("
                trajectory_linestring = "LINESTRING ("
                for k in range(len(decoded_polyline)):
                        decoded_polyline_loop = str(decoded_polyline[k])
                        decoded_polyline_loop = decoded_polyline_loop[1:len(decoded_polyline_loop)-1]
                        blankspace = decoded_polyline_loop.find(" ")
                        #my_dict_output[f'step_pathway{k}'] = f"({decoded_polyline_loop[blankspace+1:len(decoded_polyline_loop)]},{decoded_polyline_loop[0:blankspace-1]})"

                        if k == len(decoded_polyline)-1:
                            lng_lat = f"({decoded_polyline_loop[blankspace+1:len(decoded_polyline_loop)]} {decoded_polyline_loop[0:blankspace-1]})"
                            lng_lat_linestring = f"{decoded_polyline_loop[blankspace+1:len(decoded_polyline_loop)]} {decoded_polyline_loop[0:blankspace-1]}"
                        else:
                            lng_lat = f"({decoded_polyline_loop[blankspace+1:len(decoded_polyline_loop)]} {decoded_polyline_loop[0:blankspace-1]}),"
                            lng_lat_linestring = f"{decoded_polyline_loop[blankspace+1:len(decoded_polyline_loop)]} {decoded_polyline_loop[0:blankspace-1]},"
                            
                        
                        trajectory_multipoint = trajectory_multipoint+lng_lat
                        trajectory_linestring = trajectory_linestring+lng_lat_linestring
                        ## Sample LINESTRING FORMAT:
                        ##LINESTRING (74.3972369 31.4837934,74.3965815 31.484379,74.3939482 31.4823563,74.3943417 31.4818988,74.3973884 31.4789894,74.4070362 31.4713599,74.4061082 31.4705868,74.4056551 31.4683772,74.4181696 31.4661234,74.418036 31.4654491)

                trajectory_multipoint = trajectory_multipoint + ")"
                trajectory_linestring = trajectory_linestring + ")"
                
                my_dict_output['Trajectory_Multipoint'] = trajectory_multipoint
                my_dict_output['Trajectory_Linestring'] = trajectory_linestring

                route_counter += 1
                master_list.append(my_dict_output)
                
            return master_list    

        #master_data_times = Directions_Times(self,r_json)
        #master_data_paths = Directions_Trajectory(self,r_json,mode=mode)
        
        #return master_data_times,master_data_paths
        return None

        
