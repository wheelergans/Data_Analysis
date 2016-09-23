zipname = 'RX_1_Data'
myzip = zipfile.ZipFile(zipname+'.zip', 'r')
dflist = list()
for filename in myzip.namelist():
	if '.CSV' in filename:
		try:
			dflist.append(pd.read_csv(filename))
			print('read')
		except:
			print('could not read file: '+ filename)

import os
import pytz
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
	if os.path.isdir(folder):
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

#Code for after code update			
			#check to see if there is a _NME file for the log number
			if (log_number+'_NME.CSV') in file_list:
				#if NME file then need to correlate millis to GPS time from NME file

				# 1 Find first line in NME with good timestamp on GPRMC
				# and calculate start time when millis = 0
				print('parsing log number: '+ log_number)
				if(log_number+'_POW.CSV') not in file_list:
					continue
				temppow=pd.read_csv(log_number+'_POW.CSV')
				if (log_number+'_RF.CSV') in file_list: #RF file only present if packets are lost
					temprf = pd.read_csv(log_number+'_RF.CSV')
					rf_flag = True	
								
				with open(log_number+'_NME.CSV') as infile:
					for line in infile:
						if 'GPRMC' in line:
							line = line.split(',')
							if line[2] and line[10]:
								first_epoch = dt.datetime.strptime(line[2]+','+line[10],"%H%M%S.%f,%d%m%y").strftime('%s')
								#first_epoch = pytz.utc.localize(first_time)
								first_millis = int(line[0][line[0].find('"')+1:])
								break

					temppow.columns = temppow.columns.str.replace(' ','_')
					if rf_flag:
						temprf.columns = temprf.columns.str.replace(' ','_')
					#calculate timestamp from start time and millis and set to index timestamp for power DF
					
					temppow.index = (dt.datetime.fromtimestamp(float(first_epoch)) + (temppow['millis']-first_millis).apply(lambda x: dt.timedelta(milliseconds = float(x))))-dt.timedelta(hours = 8)
					#(temppow['millis']-first_millis).apply(lambda x: dt.timedelta(milliseconds = float(x)))
					temppow.index.name = 'timestamp'

					#calculate timestamp from start time and millis and set to index timestamp for RF DF
					if rf_flag:
						temprf.index = dt.datetime.fromtimestamp(float(first_epoch)) + (temprf['ard_millis']-first_millis).apply(lambda x: dt.timedelta(milliseconds = float(x)))
						temprf.index.name = 'timestamp'


					#add log numbers to DFs
					temppow['log_num'] = log_number
					if rf_flag:
						temprf['log_num'] = log_number

					#append temp DFs to logs
					powdata = powdata.append(temppow)
					if rf_flag:
						rfdata = rfdata.append(temprf)

					#delete temp DFs
					del temppow
					if rf_flag:
						del temprf
					rf_flag = False

#Code for before NME switch
			elif (log_number+'_GPS.CSV') in file_list:
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
					start_time = dt.datetime.fromtimestamp(epoch_start)

					#calculate timestamp from epoch time for GPS DF
					tempgps.index = tempgps['GPS_Epoch_Time'].apply(lambda x: dt.datetime.fromtimestamp(float(x)))
					tempgps.index.name = 'timestamp'

					#add log number to gps df
					tempgps['log_num'] = log_number

					#append to DF
					gpsdata = gpsdata.append(tempgps)

					#delete temp df
					del tempgps

					#calculate timestamp from start time and millis and set to index timestamp for power DF
					temppow.index = start_time + temppow['millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))
					temppow.index.name = 'timestamp'

					#calculate timestamp from start time and millis and set to index timestamp for RF DF
					if rf_flag:
						temprf.index = dt.datetime.fromtimestamp(epoch_start) + temprf['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))
						temprf.index.name = 'timestamp'


					#add log numbers to DFs
					temppow['log_num'] = log_number
					if rf_flag:
						temprf['log_num'] = log_number

					#append temp DFs to logs
					powdata = powdata.append(temppow)
					if rf_flag:
						rfdata = rfdata.append(temprf)

					#delete temp DFs
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
gpsdata.to_hdf('gps_store.h5','powdata',complib = 'blosc',complevel=9)
print('logging powdata to csv')
powdata.to_hdf('pow_store.h5','powdata',complib = 'blosc',complevel=9)
print('logging rfdata to csv')
rfdata.to_hdf('rf_store.h5','table',complib = 'blosc',complevel=9)

os.chdir(cwd)






