import os
import pandas as pd
import datetime as dt
import numpy as np
import sqlite3

data_dir_path = '/Users/wheelergans/Desktop/DATABASE_TEST'
sd_dir_path = '/Users/wheelergans/Desktop/SD_TEST'

def check_for_sd(void):
    #todo: check for sd return path
    return(sd_dir_path)


#todo: get spotter ID from log file



if __name__ == '__main__':
    _sd_dir_path = check_for_sd()
    if os.path.exists(_sd_dir_path):
        file_list = os.listdir(_sd_dir_path)
        file_list.sort()

        # Define list to hold log numbers
        log_list = list()
        for filename in file_list:
            if '_' in filename and 'DS' not in filename:
                end_index = filename.index('_')
                log_number = filename[:end_index]
                if log_number not in log_list:
                    log_list.append(log_number)
    else:
        print("No SD card present!")
        #todo: return error code





