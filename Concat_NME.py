import os
import pandas as pd
import datetime as dt

'''
#prompt user for data director
datadir = input('Enter the data director path: ')
#change to data directory
os.chdir(datadir)
print('path changed to : '+ datadir)'''

cwd = os.getcwd()
#try:
#setup DFs
powdata = pd.DataFrame()
gpsdata = pd.DataFrame()
rfdata = pd.DataFrame()

#Get folder list and sort
folder_list = os.listdir()
folder_list.sort()
for folder in folder_list:
	if '.DS_Store' not in folder:
		print('getting data from folder: '+folder)
		os.chdir(folder)

		# Get file list and sort 
		file_list = os.listdir()
		file_list.sort()

		# Define list to hold log numbers
		log_list = list()

		# Get all unique log numbers into list
		for filename in file_list:
			if '_' in filename:
				end_index = filename.index('_') 
				log_number = filename[:end_index]
				if log_number not in log_list:
					log_list.append(log_number)

		for log_number in log_list:
			rf_flag = False

			# Check to see if there is a GPS file for a given log number and if so
			# read in CSV for log number into temp DF
			if (log_number+'_NME.CSV') in file_list:
				

			if (log_number+'_GPS.CSV') in file_list:
				print('parsing log number: '+ log_number)
				tempgps = pd.read_csv(log_number+'_GPS.CSV')
				if(log_number+'_POW.CSV') not in file_list:
					continue
				temppow=pd.read_csv(log_number+'_POW.CSV')
				if (log_number+'_RF.CSV') in file_list: #RF file only present if packets are lost
					temprf = pd.read_csv(log_number+'_RF.CSV')
					rf_flag = True



				if len(tempgps[tempgps['GPS Epoch Time'] >= 1400000000]):

					#remove white space from column header
					tempgps.columns = tempgps.columns.str.replace(' ','_')
					temppow.columns = temppow.columns.str.replace(' ','_')
					if rf_flag:
						temprf.columns = temprf.columns.str.replace(' ','_')

					#toss out any gps data with bad fix
					tempgps = tempgps[tempgps.GPS_Epoch_Time >= 1400000000]
					
					#sort by timestamp
					tempgps = tempgps.sort_values(['GPS_Epoch_Time'])

					#calculate start time from gps file
					epoch_start = tempgps.GPS_Epoch_Time.iloc[0]-(tempgps.ard_millis.iloc[0]/1000) 

					#calculate timestamp from start time and millis and set to index timestamp for power DF
					temppow.index = dt.datetime.fromtimestamp(epoch_start) + temppow['millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))
					temppow.index.name = 'timestamp'

					#calculate timestamp from start time and millis and set to index timestamp for RF DF
					if rf_flag:
						temprf.index = dt.datetime.fromtimestamp(epoch_start) + temprf['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))
						temprf.index.name = 'timestamp'

					#calculate timestamp from epoch time for GPS DF
					tempgps.index = tempgps['GPS_Epoch_Time'].apply(lambda x: dt.datetime.fromtimestamp(float(x)))
					tempgps.index.name = 'timestamp'

					#add log numbers to DFs
					temppow['log_num'] = log_number
					tempgps['log_num'] = log_number
					if rf_flag:
						temprf['log_num'] = log_number

					#append temp DFs to logs
					powdata = powdata.append(temppow)
					gpsdata = gpsdata.append(tempgps)
					if rf_flag:
						rfdata = rfdata.append(temprf)

				#delete temp DFs
				del tempgps
				del temppow
				if rf_flag:
					del temprf
				rf_flag = False
		os.chdir(cwd)

#sort final dataframes
powdata.sort_index()
gpsdata.sort_index()
rfdata.sort_index()
#except:
#	print('error running script')
#	os.chdir(cwd)


#log dfs to csv
print('logging gpsdata to csv')
gpsdata.to_hdf('gps_store.h5','table',complib = 'blosc',complevel=5)
print('logging powdata to csv')
powdata.to_hdf('pow_store.h5','table',complib = 'blosc',complevel=5)
print('logging rfdata to csv')
rfdata.to_hdf('rf_store.h5','table',complib = 'blosc',complevel=5)

os.chdir(cwd)






