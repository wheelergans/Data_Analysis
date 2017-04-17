import os
import pytz
import pandas as pd
import datetime as dt 
import matplotlib.pylab as plt

file_list = os.listdir()
file_list.sort()

testinfo = open("testinfo.txt", "w")

# Define list to hold log numbers
log_list = list()
for filename in file_list:
	if '_' in filename and 'DS' not in filename:
		end_index = filename.index('_') 
		log_number = filename[:end_index]
		if log_number not in log_list:
			log_list.append(log_number)

Incomplete_files =dict()
short_files = dict()

#define data structs
powdata = pd.DataFrame()
gpsdata = pd.DataFrame()
nmeadata = pd.DataFrame()
sysdata = pd.DataFrame()
fdbdata = pd.DataFrame()
fltdata = pd.DataFrame()
mesdata = pd.DataFrame()
spcdata = pd.DataFrame()


#concat log numbers and add timestamps - NOTE: timestamps are assigned from first gps time correlation 
#to millis for each log file. Over larger log file there will be some drift
for log_number in log_list:

	#gps concat
	if(log_number+'_GPS.CSV') in file_list:
		tempgps = pd.read_csv(log_number+'_GPS.CSV')
		tempgps['Session_ID']=log_number

		#toss out any gps data with bad fix
		tempgps = tempgps[tempgps['GPS Epoch Time'] >= 1400000000]
		
		#sort by timestamp
		tempgps = tempgps.sort_values(['GPS Epoch Time'])

		#calculate start time from gps file
		epoch_start = tempgps['GPS Epoch Time'].iloc[0]-(tempgps.ard_millis.iloc[0]/1000) 
		start_time = dt.datetime.fromtimestamp(epoch_start)
		#append to DF
		gpsdata = gpsdata.append(tempgps)
	else:
		continue

	#pow concat
	if(log_number+'_POW.CSV') in file_list:
		temppow = pd.read_csv(log_number+'_POW.CSV')
		temppow['Session_ID']=log_number
		temppow.index = start_time + temppow['millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		powdata = powdata.append(temppow)

	#nmea concat
	if(log_number+'_NME.CSV') in file_list:
		if os.stat(log_number+'_NME.CSV').st_size<9000000:
			short_files[log_number] = os.stat(log_number+'_NME.CSV').st_size/1000

		tempnmea = pd.read_csv(log_number+'_NME.CSV')
		tempnmea['Session_ID']=log_number
		tempnmea.index = start_time + tempnmea['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		nmeadata = nmeadata.append(tempnmea)

	#sys concat
	if(log_number+'_SYS.CSV') in file_list:
		tempsys = pd.read_csv(log_number+'_SYS.CSV')
		tempsys['Session_ID']=log_number
		tempsys.index = start_time + tempsys['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		sysdata = sysdata.append(tempsys)

	#fdb concat
	if(log_number+'_FDB.CSV') in file_list:
		tempfdb = pd.read_csv(log_number+'_FDB.CSV')
		tempfdb['Session_ID']=log_number
		tempfdb.index = start_time + tempfdb['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		fdbdata = fdbdata.append(tempfdb)

	#flt concat
	if(log_number+'_FLT.CSV') in file_list:
		tempflt = pd.read_csv(log_number+'_FLT.CSV')
		tempflt['Session_ID']=log_number
		tempflt.index = start_time + tempflt['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		fltdata = fltdata.append(tempflt)

	#mes concat
	if(log_number+'_MES.CSV') in file_list:
		tempmes = pd.read_csv(log_number+'_MES.CSV')
		tempmes['Session_ID']=log_number
		tempmes.index = start_time + tempmes['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		mesdata = mesdata.append(tempmes)




#clean up GPS DF
gpsdata.columns = gpsdata.columns.str.replace(' ','_')
gpsdata.index = gpsdata['GPS_Epoch_Time'].apply(lambda x: dt.datetime.fromtimestamp(float(x)))
gpsdata.index.name = 'timestamp'

#clean up POW DF
powdata.columns = powdata.columns.str.replace(' ','_')
powdata.index.name = 'timestamp'

#clean up SYS DF
sysdata.columns = sysdata.columns.str.replace(' ','_')
sysdata.index.name = 'timestamp'

with open('testinfo.txt','w') as testinfo:
	testinfo.write("Start Time: ")
	testinfo.write(dt.datetime.fromtimestamp(gpsdata.sort_index().iloc[0].GPS_Epoch_Time).ctime())
	testinfo.write("\n")
	testinfo.write("End Time: ")
	testinfo.write(dt.datetime.fromtimestamp(gpsdata.sort_index().iloc[-1].GPS_Epoch_Time).ctime())
	testinfo.write("\n")
	testinfo.write("File Indexes: ")	
	testinfo.write(str(len(log_list)))
	
	testinfo.write("Incomplete File Indexes: ")
	testinfo.write("\n")
	testinfo.write("Short file indexes: ")
	testinfo.write(pickle.dump(short_files, testinfo, pickle.HIGHEST_PROTOCOL))
	testinfo.write("\n")

        

	testinfo.write("\n")

	testinfo.write("\n")
	testinfo.write("\n")
	testinfo.write("Errors Logged:")
	testinfo.write("\n")
	testinfo.write(sysdata[sysdata.type == 'ERROR'].to_string())



powdata.to_csv("powdata.CSV")
gpsdata.to_csv("gpsdata.CSV")
nmeadata.to_csv("nmeadata.CSV")
sysdata.to_csv("sysdata.CSV")
fdbdata.to_csv("fdbdata.CSV")
fltdata.to_csv("fltdata.CSV")
mesdata.to_csv("mesdata.CSV")



'''
	#spc concat
	if(log_number+'_SPC.CSV') in file_list:
		tempspc = pd.read_csv(log_number+'_SPC.CSV')
		tempspc['Session_ID']=log_number
		tempspc.index = start_time + tempspc['ard_millis'].apply(lambda x: dt.timedelta(milliseconds = float(x)))

		#append to DF
		spcdata = spcdata.append(temppow)






