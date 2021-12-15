import pandas as pd 

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

# path = "polyy.csv"
# DF = pd.read_csv(path)
# list_poly = DF.values.tolist()
# list_latlng = []

# for elem in list_poly:
#     a = decode_polyline(''.join(elem))
#     list_latlng.append(a)
    

# list_plot = [(31.55968, 74.31381), (31.55964, 74.31372), (31.55934, 74.31302), (31.55918, 74.31263), (31.55915, 74.31255), (31.55911, 74.31247), (31.55905, 74.31238), (31.559, 74.3123), (31.55896, 74.31224), (31.55894, 74.31217), (31.55893, 74.31212), (31.55891, 74.31195), (31.5589, 74.31183), (31.55887, 74.3115), (31.55886, 74.31121), (31.55888, 74.31102), (31.55889, 74.311), (31.55899, 74.31076), (31.5591, 74.31028), (31.55914, 74.31016), (31.55915, 74.31008), (31.55916, 74.31004), (31.55915, 74.30999), (31.55914, 74.30992), (31.5591, 74.3096), (31.55909, 74.30951), (31.55907, 74.30919)]


# DF = pd.DataFrame(list_plot)


# DF.to_csv("Testing path.csv",index=False)

overview_polyline =  "ctr_Eq}qdMY`B[rAYj@wBnCwAdBa@t@YXy@x@g@R_Bp@uAl@]P?H?Hg@zAYfAK`AEpA@`@Nt@~@nGf@bCu@P_@BC@"

coordinates = decode_polyline(overview_polyline)
