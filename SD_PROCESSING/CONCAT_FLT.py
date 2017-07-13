#command line instructions:
#	1. Move CONCAT_FLT to SD data directory
#	2. From data directory in terminal 'Python3 CONCAT_FLT.py'

#python requirements
#-Python 3 distribution
#-Scipy distribution including pandas see https://www.scipy.org/

import os
import pandas as pd

file_list = os.listdir()
file_list.sort()

fltdata = pd.DataFrame()

# Define list to hold log numbers
for filename in file_list:
    if '_FLT' in filename:
        # append to fltdata
        fltdata = fltdata.append(pd.read_csv(filename, index_col=False))

fltdata = fltdata.drop('ard_millis',axis=1)
fltdata.to_csv('FLT_DATA.CSV')