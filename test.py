import pandas as pd

col_list = ["country", "capital", "lat", "lon", "code", "continent"]

data = pd.read_csv('countries.csv', error_bad_lines=False, encoding='cp1252', warn_bad_lines=False, sep=';',
                   usecols=col_list, na_filter=False)


min_lat = 12.726084296948185
min_lon = -174.0234375
max_lat = 72.44879155730672
max_lon = -33.3984375

visible = data.loc[(data['lat'].between(min_lat,max_lat, inclusive=False)) &
                   (data['lon'].between(min_lon, max_lon, inclusive=False))]

print(visible)

