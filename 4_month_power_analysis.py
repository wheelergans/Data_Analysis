import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
import datetime as dt

def read_h5(filename):

	hdf=pd.HDFStore(filename)
	return hdf.get('powdata')

def calc_values():

	powdata['hum'] = powdata['hum'].convert_objects(convert_numeric = True)
	#calc powers
	powdata['sol_I'] = (powdata.loc[:,'sol_I_0':'sol_I_4'].sum(axis = 1))
	powdata['solP'] = powdata.sol_V*powdata.sol_I
	powdata['battP'] = powdata.batt_I*powdata.batt_V
	powdata['busP'] = powdata.bus_I*powdata.bus_V
	powdata['DCP'] = powdata.DC_V*powdata.DC_I

	#fill system efficiency column with nan
	powdata['system_n'] = np.nan

	#DF for positive batt P
	temp=powdata[powdata['battP']>=0]

	#efficiency calculation for positive batt power
	powdata['system_n'] = powdata['system_n'] + (temp.battP+temp.busP)/(temp.solP)

	#DF for negative batt P
	temp=powdata[powdata['battP']<0]

	#efficiency calculation for negative batt power
	powdata['system_n'] = powdata['system_n'] + (temp.busP)/(temp.solP+temp.battP)

	maximums = powdata.max()
	minimums =powdata.min()
	means = powdata.mean()
	values = pd.concat([maximums,minimums,means],axis=1)
	values.columns = ['maximums','minimums','means']
	return values

def temp_hum(DF):
	
	#temp and humidity
	#title = 'Humidity and Temperature'
	ax = DF[['temp','hum']].resample('1D',how = 'mean').plot(figsize = (14,7),legend=True,secondary_y =['hum'],linewidth =1,grid = True,mark_right = True)
	ax.set_ylabel('temp (C)')
	ax.right_ax.set_ylabel('Relative Humidity')
	ax.set_xlabel('')
	ax.axhline(DF['temp'].mean(),color = 'blue',lw=2,linestyle = '--')
	ax.right_ax.axhline(DF['hum'].mean(),color = 'green',lw=2,linestyle = '--')

	#lgd = ax.legend(loc='upper left')

	plt.savefig('temp_hum.png')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)

def charge_time():
	charge_times = pd.DataFrame(index =powdata['timestamp'].map(pd.Timestamp.date).unique() )
	
	for single_day in powdata['timestamp'].map(pd.Timestamp.date).unique():
		print(single_day)
		temp = powdata.sort_index().ix[single_day:single_day+dt.timedelta(days=1)]
		charge_times.set_value(single_day,'peak_charge',temp.battP.max())
		if not temp[temp['stat']==180].empty:
			charge_start = temp[temp['battP']>0].index[0]
			charge_end = temp[temp['stat']==180].index[0]
			charge_dur = charge_end-charge_start
			charge_times.set_value(single_day,'charge_dur',charge_dur)
		else:
			print('Did not reach full charge on: '+ single_day.strftime("%Y-%m-%d"))
	charge_times['minutes'] = charge_times['charge_dur'].astype('timedelta64[m]')	


def plot_charge_times():

	#define receiver on off dates
	rec_off= dt.date(2016,6,3)
	rec_on = dt.date(2016,6,16)

	#best fit line
	'''x = np.arange(charge_times['minutes'].dropna().size)
	fit = np.polyfit(x,charge_times['minutes'].dropna(),1)
	fit_fn = np.poly1d(fit)
	ax = plt.plot(charge_times.dropna(subset=['minutes']).index,fit_fn(x),'k-')'''

	#plot line and points
	ax = charge_times['minutes'].plot(figsize = (14,7),legend=True)
	charge_times['minutes'].plot(ax = ax,style='o',legend=True)

	#add average line
	ax.axhline(charge_times['minutes'].mean(),color = 'green',lw=2,linestyle = '--')

	#plot vertical lines where receiver off
	ax.axvline(rec_off,color = 'red',lw=2,linestyle = '--')
	ax.axvline(rec_on,color = 'red',lw=2,linestyle = '--')

	ax.set_ylabel('Time Until Full Charge')

def plot_peak_charge():
	#define receiver on off dates
	rec_off= dt.date(2016,6,3)
	rec_on = dt.date(2016,6,16)
	ax = charge_times['peak_charge'].plot(figsize = (14,7),legend=True)
	charge_times['peak_charge'].plot(ax = ax,style = 'o',legend=True)
	#add average line
	ax.axhline(charge_times['peak_charge'].mean(),color = 'green',lw=2,linestyle = '--')

	#plot vertical lines where receiver off
	ax.axvline(rec_off,color = 'red',lw=2,linestyle = '--')
	ax.axvline(rec_on,color = 'red',lw=2,linestyle = '--')

	ax.set_ylabel('Peak Batt Power (W)')
	plt.savefig(peak_charge)

def plot_sys_powers(DF,resample_int):
	rec_off= dt.date(2016,6,3)
	rec_on = dt.date(2016,6,16)

	#System Powers
	DF = DF.resample(resample_int,how = 'mean')
	title = 'System Power'
	ax = DF[['solP','battP','busP']].plot(figsize = (14,7),title = title,grid = True)
	ax.set_ylabel('Watts')
	ax.set_xlabel('')
	ax.axhline(DF['solP'].mean(),color = 'blue',lw=1,linestyle = '--')
	ax.axhline(DF['battP'].mean(),color = 'green',lw=1,linestyle = '--')
	ax.axhline(DF['busP'].mean(),color = 'red',lw=1,linestyle = '--')

	#plot vertical lines where receiver off
	ax.axvline(rec_off,color = 'red',lw=2,linestyle = '--')
	ax.axvline(rec_on,color = 'red',lw=2,linestyle = '--')

	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')




start = dt.datetime(2016,4,21)
stop = dt.datetime(2016,6,2)


powdata=read_h5('pow_store.h5')
values = calc_values()
temp_hum(powdata)
	
	rec_off= dt.date(2016,6,3)
	rec_on = dt.date(2016,6,16)
	#System Powers
	temp = temp.resample('3T',how = 'mean')
	title = 'Batt Voltage'
	ax = temp[['batt_V']].plot(figsize = (14,7),title = title,grid = True)
	ax.set_ylabel('Volts')
	ax.set_xlabel('')
	
	#plot vertical lines where receiver off
	ax.axvline(rec_off,color = 'red',lw=2,linestyle = '--')
	ax.axvline(rec_on,color = 'red',lw=2,linestyle = '--')

	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')
