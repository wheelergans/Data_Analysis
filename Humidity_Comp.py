drag = pd.read_csv('0379_POW.CSV')
drag = drag[drag['epoch_time']>0]
drag.index = drag['epoch_time'].apply(lambda x:dt.datetime.fromtimestamp(x))


ref = pd.read_csv('2012_POW.CSV')
ref = ref[ref['epoch_time']>0]
ref.index = ref['epoch_time'].apply(lambda x:dt.datetime.fromtimestamp(x))

ax = drag[['hum','temp']].plot(style = '--')
ref[['hum','temp']].plot(ax =ax)
ax.legend(labels=handles)


handles = ['hum (drag)', 'T (drag)', 'hum (ref)', 'T (ref)']

start = dt.datetime(2017,5,4,12)
stop = dt.datetime(2017,5,4,1)