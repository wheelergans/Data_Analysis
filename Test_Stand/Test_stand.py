import pandas as pd 
import pytz
import matplotlib as plt
import scipy
import datetime as dt
import os

#read in two Piksi log files
piksi_v = pd.read_csv('velocity_log_20160503-150704.csv',index_col = 'time',parse_dates = True)
piksi_pos = pd.read_csv('position_log_20160503-150704.csv',index_col = 'time',parse_dates = True)

#merge files based on time index and return piksi_data dataframe
piksi_data = pd.merge(piksi_v, piksi_pos,left_index = True,right_index = True)

#read in 
ts_raw = pd.read_csv("filename",sep = "\n",header = None)

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
ts_log = pd.DataFrame({'date':date[0],'time':time[0],'x_pos':x_pos[0],'y_pos':y_pos[0]})

#recast x and y values from string to float
ts_log['x_pos'] = ts_log['x_pos'].astype(float)
ts_log['y_pos'] = ts_log['y_pos'].astype(float)

#Create datetime time stamp from date and time columns
ts_log['timestamp'] = pd.to_datetime(date_time[0])

#Calculate average timestep - to do throw out garbage timestep data

ts_log['deltaT'] = (ts_log['timestamp']-ts_log['timestamp'].shift()).fillna(0)

#check to see if any timesteps are > 1 and print out indeces
time_gap_err = ts_log[ts_log['deltaT']>dt.timedelta(seconds =1)]
if(len(time_gap_err)):
	for index in time_gap_err.index:
		print("time gap error at index")
		print(index)

#toss out data with big time steps
new_start_index = max(time_gap_err.index)+1
ts_log=ts_log[new_start_index:]

steps = len(ts_log[ts_log['deltaT']==dt.timedelta(seconds=1)])
average_steps = len(ts_log)/steps #holds average number of data points/second

timestep = dt.timedelta(seconds = 1)/average_steps

#update timestamp column with proper timesteps

#find first 1 second jump 
jumps = ts_log[ts_log['deltaT']==dt.timedelta(seconds =1)]
start_index = jumps.index[0]

ts_log = ts_log[start_index:].reset_index(inplace = True,drop = True)






