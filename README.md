# Google-Maps-Platform-API
Python script for calculating dynamic spatio-temporal travel times!
Available modules:
1. Getting geocoded lat lng pairs against a text based address (GeoCoding API)
2. Find Place from Text string in the form of lat lng pairs (GeoCoding API)
3. Nearby search to provide matched locations in a user defined buffer radius (GeoCoding API)
4. Calculate Origin-Destination Matrix using DistanceMatrixAPI. Takes a .csv file input of lat_lng pairs, converts it into a Pandas DataFrame followed by fixed sized buckets of 10 pairs for every request generated. Outputs a .csv file having an O-D matrix 
5. Calculate travel times in the form of an O-D matrix as well as pathways using Directions API. Takes a .csv file input of lat_lng pairs, converts it into a Pandas DataFrame followed by indexing and slicing pairs for individual API requests. Outputs the data in a .csv file or a Well Known Text (WKT) format file that can be visualized directly in ArcGIS/QGIS. Included normalized travel times for monitoring traffic congestions 
