import pandas as pd 
import pytz
import matplotlib as plt
import scipy
import datetime as dt
import os
import numpy as np


#---------------------------------------------------------
#---------------------------------------------------------
def TS_log(filename):
	name = filename
	#read in 
	ts_raw = pd.read_csv(filename,sep = "\n",header = None)

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

	ts_log.deltaT[] = ts_log['timestamp'].diff()


	#check to see if any timesteps are > 1 and print out indeces
	big_gap = ts_log[ts_log['deltaT']>dt.timedelta(seconds =1)]

	if(len(big_gap)):
		for index in big_gap.index:
			print("time gap error at index: "),print(index)


	ts_log = ts_log[max(big_gap.index)+1:]

	#find first index for which there is 1s timestep
	temp = ts_log[ts_log.deltaT == dt.timedelta(seconds=1)]
	new_start_index = temp.index[0]
	print("new start index: "),print(new_start_index)
	ts_log = ts_log[new_start_index:]
	

	steps = len(ts_log[ts_log['deltaT']==dt.timedelta(seconds=1)])
	average_steps = len(ts_log)/steps #holds average number of data points/second

	timestep = dt.timedelta(seconds = 1)/average_steps

	#update timestamp column with proper timesteps

	
	ts_log.reset_index(inplace = True,drop = True)
	#to do - change from adding by multiplier and instead add to original timestamp

	ts_log.index= ts_log.index*timestep+ts_log.timestamp[0]
	ts_log.index.name = 'timestamp'
	del ts_log['timestamp']

	#length = len(ts_log.ts_x_pos)
	#ts_log['x_disp'] = np.empty([length,]) 
	#ts_log.x_disp[1:] +=np.diff(ts_log.ts_x_pos)
	#ts_log['y_disp'] = np.empty([length,]) 
	#ts_log.y_disp[1:] +=np.diff(ts_log.ts_y_pos)

	#to do - change from dividing by average steps to past time step
	#ts_log['x_vel'] = ts_log.x_disp/(1/average_steps)
	#ts_log['y_vel'] = ts_log.y_disp/(1/average_steps)

	name = name + "_log.csv"
	#log both DF to CSV
	ts_log.to_csv(name)

#------------------------------------------------------------
TS_log('timePositionLog_5-11-2016_Ublox_Raw_circle_70cm_radius_x25.txt')
TS_log('timePositionLog_5-11-2016_Ublox_Raw_jonswap_long.txt')

ts_log = pd.read_csv('ts_log.csv')

'''

#create new date range from test stand range with evenly spaced 5 hz timestamps
st = ts_log.index[0]
en = ts_log.index[len(ts_log.index)-1]
new_index = pd.date_range(st,en,freq = '100L')

'''




