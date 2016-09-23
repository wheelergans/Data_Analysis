import pandas as pd 

rfdata = pd.read_csv('RF_LOG.CSV',index_col = 1,parse_dates = True)
rfdata['deltaT'] = rfdata.index
rfdata['deltaT'] = rfdata['deltaT'].diff()
rfdata['count'] = range(1,len(rfdata)+1,1)



