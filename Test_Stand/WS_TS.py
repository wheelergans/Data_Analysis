import pandas as pd 
import pytz
import matplotlib as plt
import scipy
import datetime as dt
import os
import numpy as np

def GPS_Concat(filepath):
#to do 
#- identify gaps in gps timestamp
#- filename should represent time and date of log in filename or file info??
	
	#record start directory
	start_dir = os.getcwd()
	print(start_dir)
	#change path to filepath
	os.chdir(filepath)

#to do - check remove any files from list that do not have correct suffix
	#get file list and sort 
	file_list = os.listdir(filepath)
	file_list.sort()

	#check if log file exists
	if 'gps_log.csv' in file_list:
		return 

	#create GPS data dataframe
	gps_data = pd.DataFrame()

	#read in all files into data frame
	for filename in file_list:
			if 	"GPS" in filename:
				end_index = filename.index('_')
				log_number = filename[:end_index]
				temp = pd.read_csv(filename)
				temp['log number'] = log_number
				gps_data = gps_data.append(temp)

	#remove white space from column header
	gps_data = gps_data.rename(columns =lambda x: x.replace(' ','_'))

	#toss out with bad fix
	gps_data = gps_data[gps_data.GPS_Epoch_Time >= 1400000000]
	
	#sort by timestamp
	gps_data = gps_data.sort_values(['GPS_Epoch_Time'])

	#log concatenated dataframe to new CSV
	gps_data.to_csv('gps_log.csv')

	#change back to cwd
	os.chdir(start_dir)
#---------------------------------------------------------
#---------------------------------------------------------
def TS_log(filename):
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

#------------------------------------------------------------
TS_log('teststand_05-03-2016_logfile_swift_system.txt')
GPS_Concat('/Users/wheelergans/Desktop/Test/WS')
ts_log = pd.read_csv('ts_log.csv')
WS_data = pd.read_csv('gps_log.csv')

#create new date range from test stand range with evenly spaced 5 hz timestamps
st = ts_log.index[0]
en = ts_log.index[len(ts_log.index)-1]
new_index = pd.date_range(st,en,freq = '100L')

#Build new DF with relevant values from other DFs
Data = pd.DataFrame(index = new_index)
Data = pd.concat([Data,piksi_data[['GPS_Epoch_Time','lat','long','SOG_(mm/s)','COG_(deg*1000)','Vert_Vel_(mm/s)']],ts_log[['ts_x_pos','ts_y_pos']]],axis =1)
Data = Data.sort_index().interpolate('time')

#only keep data for which there is test stand data
Data = Data[np.isfinite(Data['ts_x_pos'])]

#reindex to set timestep
Data = Data.reindex(new_index)

plt.figure()
Data[['Vert_Vel(mm/s)','ts_x_pos','ts_y_pos']].plot()
plt.show()

