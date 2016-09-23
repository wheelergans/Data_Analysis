import pandas as pd 
import pytz
import matplotlib.pyplot as plt
import scipy
import datetime as dt
import os
import numpy as np
from scipy import integrate


#read in two Piksi log files
piksi_v = pd.read_csv('velocity_log_20160503-150704.csv',index_col = 'time',parse_dates = True)
piksi_pos = pd.read_csv('position_log_20160503-150704.csv',index_col = 'time',parse_dates = True)

#merge files based on time index and return piksi_data dataframe
piksi_data = pd.merge(piksi_v, piksi_pos,left_index = True,right_index = True)

#calculate displacements
piksi_data.columns = ['pyVel','pxVel','pzVel','pVel','num_sats','lat','lon','alt','num_sats','flags']
piksi_data['time'] = piksi_data.index
piksi_data['delta'] = (piksi_data['time']-piksi_data['time'].shift()).fillna(0)
piksi_data['x_disp'] = (piksi_data.delta.dt.microseconds*piksi_data['pxVel'])/10000
piksi_data['y_disp'] = (piksi_data.delta.dt.microseconds*piksi_data['pyVel'])/10000
piksi_data['z_disp'] = (piksi_data.delta.dt.microseconds*piksi_data['pzVel'])/10000


#read in 
ts_raw = pd.read_csv("teststand_05-03-2016_logfile_swift_system.txt",sep = "\n",header = None)

#read in individual slices for columns - dependent on starting with date!!
date = ts_raw.iloc[::4]
date.reset_index(inplace = True,drop = True)
time = ts_raw.iloc[1::4]
time.reset_index(inplace = True,drop = True)
date_time = date + ' ' + time
x_pos = ts_raw.iloc[2::4]
x_pos.reset_index(inplace = True,drop = True)
y_pos = ts_raw.iloc[3::4]
y_pos.reset_index(inplace = True,drop = True)

#build log dataframe
ts_log = pd.DataFrame({'date':date[0],'time':time[0],'ts_x_pos':x_pos[0],'ts_y_pos':y_pos[0]})

#recast x and y values from string to float and convert to meters
ts_log['ts_x_pos'] = ts_log['ts_x_pos'].astype(float)/100
ts_log['ts_y_pos'] = ts_log['ts_y_pos'].astype(float)/100

#Create datetime time stamp from date and time columns
ts_log['timestamp'] = pd.to_datetime(date_time[0])

#Calculate average timestep - to do throw out garbage timestep data

ts_log['deltaT'] = (ts_log['timestamp']-ts_log['timestamp'].shift()).fillna(0)

#check to see if any timesteps are > 1 and print out indeces
time_gap_err = ts_log[ts_log['deltaT']>dt.timedelta(seconds =1)]
if(len(time_gap_err)):
	for index in time_gap_err.index:
		print("time gap error at index: "),print(index)
		

#toss out data with big time steps
new_start_index = max(time_gap_err.index)+1
ts_log=ts_log[new_start_index:]

steps = len(ts_log[ts_log['deltaT']==dt.timedelta(seconds=1)])
average_steps = len(ts_log)/steps #holds average number of data points/second

timestep = dt.timedelta(seconds = 1)/average_steps

#update timestamp column with proper timesteps

#find first 1 second jump 
#to do - check this
jumps = ts_log[ts_log['deltaT']==dt.timedelta(seconds =1)]
start_index = jumps.index[0]

ts_log = ts_log[start_index:]
ts_log.reset_index(inplace = True,drop = True)
#to do - change from adding by multiplier and instead add to original timestamp
ts_log['timestamp_fine']= ts_log.index*timestep+ts_log.timestamp[0]
ts_log.index = ts_log['timestamp_fine']
del ts_log['timestamp_fine']

length = len(ts_log.ts_x_pos)
ts_log['x_disp'] = np.empty([length,]) 
ts_log.x_disp[1:] +=np.diff(ts_log.ts_x_pos)
ts_log['y_disp'] = np.empty([length,]) 
ts_log.y_disp[1:] +=np.diff(ts_log.ts_y_pos)

#to do - change from dividing by average steps to past time step
ts_log['x_vel'] = ts_log.x_disp/(1/average_steps)
ts_log['y_vel'] = ts_log.y_disp/(1/average_steps)

#log both DF to CSV
ts_log.to_csv('ts_log.csv')
piksi_data.to_csv('piksi_data.csv')

#create new date range from test stand range with evenly spaced 5 hz timestamps
st = ts_log.index[0]
en = ts_log.index[len(ts_log.index)-1]
new_index = pd.date_range(st,en,freq = '100L')

#Build new DF with relevant values from other DFs
Data = pd.DataFrame(index = new_index)
Data = pd.concat([Data,piksi_data[['pxVel','pyVel','pzVel','pVel']],ts_log[['ts_x_pos','ts_y_pos']]],axis =1)
Data = Data.sort_index().interpolate('time')

#only keep data for which there is test stand data
Data = Data[np.isfinite(Data['ts_x_pos'])]

#reindex to set timestep
Data = Data.reindex(new_index)

#calc displacements
Data['pzDisp'] = np.nan
Data.pzDisp[1:] = integrate.cumtrapz(Data['pzVel'],x = Data.index.microsecond/1000000)
Data['ts_y_disp'] = Data['ts_y_pos'].diff()
Data['ts_x_disp'] = Data['ts_x_pos'].diff()
#plotting

#test stand x and y velocities
plt.figure()
Data[['pzVel','ts_x_pos','ts_y_pos']].plot()
plt.show()



