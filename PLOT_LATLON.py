import pandas as pd
import LatLon as ll

import matplotlib.pyplot as plt


gpsdata = pd.read_csv('gpsdata.CSV',parse_dates=True,index_col = 'timestamp')

gpsdata['latitude'] = gpsdata['lat_(deg)']+gpsdata['lat_(min)']/6000000
gpsdata['longitude'] = gpsdata['_long_(deg)']+gpsdata['long_(min)']/6000000

del gpsdata['lat_(deg)']
del gpsdata['lat_(min)']
del gpsdata['_long_(deg)']
del gpsdata['long_(min)']
