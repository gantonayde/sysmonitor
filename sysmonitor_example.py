#!/usr/bin/python3

import os
import time
import psutil
import subprocess
import pandas as pd
from datetime import datetime


MEMORY_USAGE = 80                       # Memory usage threshold in % 
NPROC = 5                               # Number of processes to log
LOG_DIR = os.getcwd()                   # Location of log files
MEM_CHECK_FREQ = int(3)                 # Memory check up frequency in seconds
LOG_SET_OFF_TIME = int(15)              # Begin logging after 15 seconds
LOG_INTERVALS = int(10*60)              # Write a new entry every 10 mins after the initial one if the memory usage continues to be > MEMORY_USAGE
T_UNDER_LOAD = {'mem': 0}               # Time under load in LOG_SET_OFF_TIME//MEM_CHECK_FREQ
SET_OFF_STEP = LOG_SET_OFF_TIME//MEM_CHECK_FREQ # Define when to start logging in the units of T_UNDER_LOAD

GENERAL_LOG_FILENAME = "general_proc_info.log"
PROC_DETAILS_FILENAME = "proc_details.log"

def get_current_time():
    '''
    Obtain current time and make it readable.
    '''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S %d/%m/%y")
    return current_time

def get_mem_usage():
    '''
    Measure memory (RSS) usage.
    '''
    memory_usage = psutil.virtual_memory().percent
    return memory_usage

def get_proc_by_memory(num_processes=NPROC):
    '''
    Get list of running process sorted by Memory Usage.
    '''
    list_of_processes = []
    list_of_attributes = ['pid', 'name', 'username', 'cwd', 'create_time', 'status', 'cpu_percent']
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           proc_info = proc.as_dict(attrs=list_of_attributes)
           # Add rss key, convert values to MB and format 'create_time'
           proc_info['rss'] = round(proc.memory_info().rss / (1024 * 1024))
           proc_info['create_time'] = datetime.fromtimestamp(proc.create_time()).strftime("%H:%M:%S %d/%m/%y")
           list_of_processes.append(proc_info)
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass
    # Sort list of dict by rss
    list_of_processes = sorted(list_of_processes, key=lambda proc_obj: proc_obj['rss'], reverse=True)
    # Convert to pandas dataframe
    df = pd.DataFrame(list_of_processes[:num_processes])
    # Set the process id as index of a process
    df.set_index('pid', inplace=True)
    # Use list of attributes to order columns
    list_of_attributes.remove('pid')
    list_of_attributes += ['rss']
    df = df.reindex(columns=list_of_attributes)
    return df

def get_details_with_shell(cmd):
    '''
    Get system/process details with shell commands.
    '''
    details  = subprocess.run(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             encoding='utf-8')
    details = details.stdout
    return details

if __name__ == '__main__':
    while True:
        memory_usage = get_mem_usage()
        if memory_usage > MEMORY_USAGE:
            T_UNDER_LOAD['mem'] += 1
            if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ) or (T_UNDER_LOAD['mem'] % int(LOG_INTERVALS//MEM_CHECK_FREQ)) == 0:
                proc_info = get_proc_by_memory()

                with open(os.path.join(LOG_DIR, GENERAL_LOG_FILENAME),'a') as log_file:
                    if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ):
                        sys_info_cmd = 'uname -a'
                        sys_info = get_details_with_shell(sys_info_cmd)
                        log_file.write(f"NEW LOG FOR SYSTEM: {sys_info}\n")
                    else:
                        log_file.write(f"CONTINUING THE LOG WHICH STARTED {((T_UNDER_LOAD['mem']*MEM_CHECK_FREQ)-LOG_SET_OFF_TIME)//60} MINUTES AGO\n")
                    log_file.write(f"TIME: {get_current_time()}\n")   
                    log_file.write(f"MEMORY USAGE: {memory_usage}%\n")
                    log_file.write(f"{proc_info.to_string(header = True, index = True)}\n\n")

                with open(os.path.join(LOG_DIR, PROC_DETAILS_FILENAME),'a') as details_log_file:
                    details_log_file.write(f"TIME: {get_current_time()}\n")
                    details_log_file.write(f"MEMORY USAGE: {memory_usage}%\n")
                    if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ):
                        details_log_file.write(f"NEW LOG\n")
                    else:
                        details_log_file.write(f"CONTINUING THE LOG WHICH STARTED {((T_UNDER_LOAD['mem']*MEM_CHECK_FREQ)-LOG_SET_OFF_TIME)//60} MINUTES AGO\n")
                    for pid in list(proc_info.index.values):
                        ps_cmd = f"ps -Flww -p {pid}"
                        ps_details = get_details_with_shell(ps_cmd)
                        details_log_file.write(f"{ps_details}\n")
                    for pid in list(proc_info.index.values):
                        proc_cmd = f"cat /proc/{pid}/status"
                        proc_status = get_details_with_shell(proc_cmd)
                        details_log_file.write(f"{proc_status}\n")
        else:
            T_UNDER_LOAD['mem'] = 0
            
        time.sleep(MEM_CHECK_FREQ)
