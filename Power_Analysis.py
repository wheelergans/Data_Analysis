
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

cwd = os.getcwd()
#prompt user for data director
datadir = os.getcwd()
#change to data directory
os.chdir(datadir)
print('path changed to : '+ datadir)

try:
	#read in csv and parse dates
	pow_data = pd.read_csv('powdata.CSV',index_col = 0,parse_dates = True)

	#calc powers
	pow_data['solP'] = pow_data.sol_V*pow_data.sol_I
	pow_data['battP'] = pow_data.batt_I*pow_data._batt_V
	pow_data['busP'] = pow_data.bus_I*pow_data.bus_V

	#fill system efficiency column with nan
	pow_data['system_n'] = np.nan

	#DF for positive batt P
	temp=pow_data[pow_data['battP']>=0]

	#efficiency calculation for positive batt power
	pow_data['system_n'] = pow_data['system_n'] + (temp.battP+temp.busP)/(temp.solP)

	#DF for negative batt P
	temp=pow_data[pow_data['battP']<0]

	#efficiency calculation for negative batt power
	pow_data['system_n'] = pow_data['system_n'] + (temp.busP)/(temp.solP+temp.battP)

	maximums = pow_data.max()
	minimums =pow_data.min()
	means = pow_data.mean()
	values = pd.concat([maximums,minimums,means],axis=1)
	values.columns = {'maximums','minimums','means'}
	values.to_csv('POWVALS.CSV')
	pow_data = pow_data.resample('10T').mean()
except:
	print('error processing CSV')

try:
	#temp and humidity
	title = 'Humidity and Temperature'
	ax = pow_data[['temp','hum']].plot(title = title,secondary_y =['hum'],linewidth =2,grid = True)
	ax.set_ylabel('temp (C)')
	ax.right_ax.set_ylabel('Hum')
	ax.set_xlabel('')
	ax.axhline(means['temp'],color = 'blue',lw=2,linestyle = '--')
	ax.right_ax.axhline(means['hum'],color = 'green',lw=2,linestyle = '--')

	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')

	#batt IV
	title = 'Battery IV'
	ax = pow_data[['batt_V','batt_I']].plot(title = title ,secondary_y =['batt_I'],linewidth =2,grid = True)
	ax.set_ylabel('Volts')
	ax.right_ax.set_ylabel('Amps')
	ax.set_xlabel('')
	ax.axhline(means['batt_V'],color = 'blue',lw=2,linestyle = '--')
	ax.right_ax.axhline(means['batt_I'],color = 'green',lw=2,linestyle = '--')
	ax.set_ylim([2,5])
	ax.right_ax.set_ylim([-.5,1.5])
	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')

	#BUS IV
	title = 'BUS IV'
	ax = pow_data[['bus_V','bus_I']].plot(title = title,secondary_y =['bus_I'],linewidth =2,grid = True)
	ax.set_ylabel('Volts')
	ax.right_ax.set_ylabel('Amps')
	ax.set_xlabel('')
	ax.axhline(means['bus_V'],color = 'blue',lw=2,linestyle = '--')
	ax.right_ax.axhline(means['bus_I'],color = 'green',lw=2,linestyle = '--')
	ax.set_ylim([2,5])
	ax.right_ax.set_ylim([0,.5])
	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')


	#SOL IV
	title = 'SOL IV'
	ax = pow_data[['sol_V','sol_I']].plot(title = title,secondary_y =['sol_I'],linewidth =2,grid = True)
	ax.set_ylabel('Volts')
	ax.right_ax.set_ylabel('Amps')
	ax.set_xlabel('')
	ax.axhline(means['sol_V'],color = 'blue',lw=2,linestyle = '--')
	ax.right_ax.axhline(means['sol_I'],color = 'green',lw=2,linestyle = '--')
	ax.set_ylim([4,8])
	ax.right_ax.set_ylim([0,1])
	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')

	#System Powers
	title = 'System Power'
	ax = pow_data[['solP','battP','busP']].plot(title = title,linewidth =2,grid = True)
	ax.set_ylabel('Watts')
	ax.set_xlabel('')
	ax.axhline(means['solP'],color = 'blue',lw=1,linestyle = '--')
	ax.axhline(means['battP'],color = 'green',lw=1,linestyle = '--')
	ax.axhline(means['busP'],color = 'red',lw=1,linestyle = '--')

	lgd = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

	plt.savefig(title, bbox_extra_artists=(lgd,), bbox_inches='tight')

	#efficiency
	title = 'System efficiency'
	ax = pow_data[['system_n']].plot(title = title,linewidth =2,grid = True)
	ax.set_xlabel('')
	ax.axhline(means['system_n'],color = 'blue',lw=2,linestyle = '--')

	plt.savefig(title)

except:
	print('error plotting')

#change back to starting directory
os.chdir(cwd)



