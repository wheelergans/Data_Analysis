import os
import pandas as pd
import datetime as dt
import csv
import matplotlib.pyplot as plt
import numpy as np
import zipfile

def concat_RX():
# only for concatting zipped data
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

rxdata = pd.concat(dflist)

def load_hd5_rx():
	hdf=pd.HDFStore('rxdata.h5')
	rxdata01 = hdf.get('rxdata01')
	rxdata01 = rxdata01[['rssi']]
	rxdata04 = hdf.get('rxdata04')
	rxdata04 = rxdata04[['rssi']]
	return rxdata04,rxdata01
##-----------------------------------
# all data now stored in rxdata.h5 file - which contains two DFs rxdata01 and rxdata04 

def process_rx(rxdata):   
	#sort index and remove garbage epoch time data points
	rxdata.sort_index(inplace=True)
	start = dt.date(2016,4,18) #start date for test to remove garbage data points
	rxdata = rxdata.ix[start:]#take only data points with datetime after start date

	rxdata['timestamp']=rxdata.index #for some reason you cannot perform operations with index so need temp timestamp column
	rxdata['delta']=rxdata.timestamp.diff(1) # get timestamp delta
	
	rxdata = rxdata[rxdata['delta']<dt.timedelta(seconds = 100)]
	del rxdata['timestamp']
	#get gap distribution
	values = rxdata['delta'].value_counts()
	values.sort_index(inplace=True)
	return rxdata,values

def plot_gaps_bar():
	ax = values.ix[.2:150].plot.bar(legend=True,figsize=(14,7))
	ax.set_yscale('log')
	#ax.set_yticks(range(0,int(values.max())+5,2))
	ax.set_title('Time Series Gap Length Distribution')
	ax.set_ylabel('# of Gaps')
	ax.set_xlabel('Time Gap (seconds)')
	handles, labels = ax.get_legend_handles_labels()
	labels = ['deck unit','harbor deployment']
	ax.legend(handles,labels)
	#plt.savefig('mins.png')

def RX_stats(rxdata):
	points = len(rxdata) #number of data points
	gap_num = len(rxdata[rxdata.delta>dt.timedelta(seconds=.25)]) #number of gaps
	gaps = rxdata[rxdata.delta>dt.timedelta(seconds=.25)]
	lost_points = (gaps.delta.sum()-len(gaps)*dt.timedelta(seconds=.2))/dt.timedelta(seconds=.2)
	print(points/(points+lost_points))


rxdata['delta']= rxdata['delta'].apply(lambda x: x.seconds+x.microseconds/1000000)
rxdata01[rxdata01['delta']>dt.timedelta(seconds =0.21)]


rxdata04,rxdata01 = load_hd5_rx()
rxdata01,values01 = process_rx(rxdata01)
rxdata04,values04 = process_rx(rxdata04)
RX_stats(rxdata01)
RX_stats(rxdata04)





print('path changed to : '+ datadir)
transmitter = '7004'
# Get file list and sort 
file_list = os.listdir()

	dflist = []
	for filename in file_list:
		if '.CSV' in filename:
			print('reading '+filename)
			temp = pd.read_csv(filename)
			dflist.append(temp)
	rxdata = pd.concat(dflist)

else:
	rawdata = pd.read_csv('RX_Log.CSV')
	rxdata =rxdata[rxdata['transmitter']==int(transmitter)]
	rxdata =rxdata[rxdata['GPS Epoch Time'] >= 1400000000]
	rxdata = rxdata.drop_duplicates(subset = 'GPS Epoch Time')

	rxdata.index = rxdata['GPS Epoch Time'].apply(lambda x: dt.datetime.fromtimestamp(float(x)))
	rxdata = rxdata.sort_index()
	del rxdata['ard millis']

	rxdata['delta'] = rxdata['GPS Epoch Time'].diff()
	rxdata = rxdata[rxdata.delta<50]

	CSVdata = dict()

	CSVdata['mean delta']= rxdata.delta.mean()
	CSVdata['max time gap'] = rxdata.delta.max()
	CSVdata['min time gap'] = rxdata.delta.min()
	CSVdata['# of data points'] = len(rxdata)
	CSVdata['gaps >1s'] = len(rxdata[rxdata.delta>1])
	CSVdata['gaps >5s'] = len(rxdata[rxdata.delta>5])
	CSVdata['gaps >10s'] = len(rxdata[rxdata.delta>10])
	CSVdata['gaps >20s'] = len(rxdata[rxdata.delta>20])

	CSVdata['# of gaps'] = len(rxdata[rxdata.delta>.25])
	gaps = rxdata[rxdata.delta>.25]
	CSVdata['# of lost data points'] = sum(gaps.delta/.2)
	CSVdata['mean time gap'] = gaps.delta.mean()
	CSVdata['percent throughput'] = CSVdata['# of data points']/(CSVdata['# of lost data points']+CSVdata['# of data points'])

	writer = csv.writer(open('RFVALS.csv', 'w'))
	for key, value in CSVdata.items():
	   writer.writerow([key, value])

	gaps.delta = gaps.delta.round(1)

	#plot showing 1s spaced interference
	ax = gaps.delta.plot(kind ='hist',bins = np.arange(.4,round(CSVdata['max time gap']),.2),logy=True,alpha = 0.5)
	plt.xticks(range(0,int(CSVdata['max time gap']),1))
	ax.set_xlabel('Time Gap (s)')
	ax.set_ylabel('# of Gaps')
	plt.savefig("1s_int"+transmitter+".png")

	#plot showing rolling mean increase
	ax = pd.rolling_mean(gaps.delta,20).plot()
	ax.set_ylabel('Average Time Gap(s)')
	plt.savefig("rollingmean"+transmitter+".png")

	#plot showing time series of time gap
	ax = gaps.delta.plot()
	ax.set_ylabel('Time Gap')
	plt.savefig("gaps"+transmitter+".png")

	#plot of cumalitive sum of data dropped in seconds
	ax = gaps.delta.cumsum().plot()
	ax.set_ylabel('Cumulative data lost (seconds)')
	plt.savefig("cumloss"+transmitter+".png")





