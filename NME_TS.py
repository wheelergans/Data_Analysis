import os
import pandas as pd
import datetime as dt


		
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


		df_list = list()
		for log_number in log_list[log_list.index(log_number)+1:]:
			print('parsing log number: '+log_number)
			
			#check to see if there is a _NME file for the log number
			if (log_number+'_NME.CSV') in file_list:
				#read in CSVish file as table and split string along commas
				temp = pd.read_table(log_number+'_NME.CSV',sep = '$GPRMC',header=None,skiprows =200)[0].str.split(',',expand=True)
				temp.replace('',np.nan,inplace=True)
				temp_vert = temp[temp[1]=='"$PUBX'][[3,14]]
				temp_vert.drop_duplicates(subset=3,keep='last',inplace=True)
				temp_vert.index = temp_vert[3]
				temp = temp[temp[1]=='"$GPRMC']
				temp.drop_duplicates( subset=2,keep='last',inplace=True)
				temp.index = temp[2]
				temp.drop(temp.columns[11:],axis=1,inplace=True)
				temp['vert']=temp_vert[14]
				temp.dropna(subset=[10],inplace=True)
				temp.index = pd.to_datetime(temp[10].astype(str)+' '+temp[2].astype(str))
				temp.drop(temp.columns[[0,1,2,3,10]],axis=1,inplace=True)
				df_list.append(temp)


				temp.index = pd.to_datetime(temp[10][temp[10]=='270716'].astype(str)+' '+temp[2].astype(str))



