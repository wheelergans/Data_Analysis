import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
plt.ion()

sysdata = pd.read_csv('sysdata.csv')
sysdata = sysdata.dropna()


sysdata.index = sysdata['timestamp'].apply(lambda x: dt.datetime.fromtimestamp(x))
#number of send failures
failures = sysdata[sysdata['message'].str.contains('send failed m')]
failures['index'] = range(1, len(failures) + 1)
succ = sysdata[sysdata['message'].str.contains('send suc')]
succ['index'] = range(1, len(succ) + 1)

failures['index'].plot(style ='o')
succ['index'].plot(style ='o')

iridata = pd.read_csv('iridata.CSV', index_col = 'ard_millis',parse_dates = True)

ax = (iridata['transmit_time']/60000).plot(kind = 'hist')
ax.set_xlabel('Transmit Time (minutes)')
ax.grid()
ax.set_title('SPOT007 (18mm antenna) Transmit Times')

iridata2 = pd.read_csv('iridata.CSV', index_col = 'ard_millis',parse_dates = True)

ax = (iridata2['transmit_time']/60000).plot(kind = 'hist')
ax.set_xlabel('Transmit Time (minutes)')
ax.grid()
ax.set_title('SPOT005 (25mm antenna) Transmit Times')

ax = (iridata2['transmit_time']/60000).plot()


iridata2 = pd.read_csv('iridata.CSV', index_col = 'ard_millis',parse_dates = True)
