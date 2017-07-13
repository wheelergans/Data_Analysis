import os
import pandas as pd
import datetime as dt
import numpy as np

file_list = os.listdir()
file_list.sort()


# Define list to hold log numbers
log_list = list()
for filename in file_list:
    if '_' in filename and 'DS' not in filename:
        end_index = filename.index('_')
        log_number = filename[:end_index]
        if log_number not in log_list:
            log_list.append(log_number)

# define data structs
powdata = pd.DataFrame()
gpsdata = pd.DataFrame()
nmeadata = pd.DataFrame()
sysdata = pd.DataFrame()
fdbdata = pd.DataFrame()
fltdata = pd.DataFrame()
mesdata = pd.DataFrame()
spcdata = pd.DataFrame()
iridata = pd.DataFrame()

# concat log numbers and add timestamps - NOTE: timestamps are assigned from first gps time correlation
# to millis for each log file. Over larger log file there will be some drift
for log_number in log_list:

    # gps concat - do gps first to get timestamp
    if (log_number + '_GPS.CSV') in file_list:
        tempgps = pd.read_csv(log_number + '_GPS.CSV')
        tempgps['Session_ID'] = log_number

        # toss out any gps data with bad fix
        tempgps = tempgps[tempgps['GPS Epoch Time'] >= 1400000000]

        # sort by timestamp
        tempgps = tempgps.sort_values(['GPS Epoch Time'])

        # calculate start time from gps file
        epoch_start = tempgps['GPS Epoch Time'].iloc[0] - (tempgps.ard_millis.iloc[0] / 1000)
        start_time = epoch_start

        # append to DF
        gpsdata = pd.concat([gpsdata,tempgps])

    else:
        start_time = np.nan

    # pow concat
    if (log_number + '_POW.CSV') in file_list:
        temppow = pd.read_csv(log_number + '_POW.CSV')
        temppow['Session_ID'] = log_number
        temppow.index = start_time + temppow['millis']/1000

        # append to DF
        powdata = pd.concat([powdata,temppow])

    # nmea concat
    if (log_number + '_NME.CSV') in file_list:
        tempnmea = pd.read_csv(log_number + '_NME.CSV')
        tempnmea['Session_ID'] = log_number

        # append to DF
        nmeadata = pd.concat([nmeadata,tempnmea])

    # sys concat
    if (log_number + '_SYS.CSV') in file_list:
        tempsys = pd.read_csv(log_number + '_SYS.CSV')
        tempsys['Session_ID'] = log_number

        if start_time == np.nan:
            tempsys['timestamp'] = np.nan
        else:
            tempsys['timestamp'] = start_time + tempsys['ard_millis']/1000
        # append to DF
        sysdata = pd.concat([sysdata,tempsys])


    # fdb concat
    if (log_number + '_FDB.CSV') in file_list:
        tempfdb = pd.read_csv(log_number + '_FDB.CSV')
        tempfdb['Session_ID'] = log_number
        tempfdb.index = start_time + tempfdb['ard_millis']/1000

        # append to DF
        fdbdata = fdbdata.append(tempfdb)

    # flt concat
    if (log_number + '_FLT.CSV') in file_list:
        tempflt = pd.read_csv(log_number + '_FLT.CSV')
        tempflt['Session_ID'] = log_number
        tempflt.index = start_time + tempflt['ard_millis']/1000

        # append to DF
        fltdata = pd.concat([fltdata,tempflt])

    # mes concat
    if (log_number + '_MES.CSV') in file_list:
        tempmes = pd.read_csv(log_number + '_MES.CSV')
        tempmes['Session_ID'] = log_number
        tempmes.index = start_time + tempmes['ard_millis']/1000

        # append to DF
        mesdata = pd.concat([mesdata,tempmes])

   # iri concat
    if (log_number + '_IRI.CSV') in file_list:
        tempiri = pd.read_csv(log_number + '_IRI.CSV')
        tempiri['Session_ID'] = log_number
        tempiri.index = start_time + tempiri['ard_millis']/1000

        # append to DF
        iridata = pd.concat([iridata,tempiri])


powdata.to_csv("powdata.CSV")
gpsdata.to_csv("gpsdata.CSV")
nmeadata.to_csv("nmeadata.CSV")
sysdata.to_csv("sysdata.CSV")
fdbdata.to_csv("fdbdata.CSV")
fltdata.to_csv("fltdata.CSV")
mesdata.to_csv("mesdata.CSV")
iridata.to_csv("iridata.CSV")


