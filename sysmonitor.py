#!/usr/bin/python

import os
import time
import psutil
import subprocess
import pandas as pd
from datetime import datetime

MEMORY_LOAD = 40                        # Memory load in % needed for logging
NPROC = 5                               # Number of processes to log
MEM_CHECK_FREQ = int(3)                 # Memory check up frequency in seconds
LOG_SET_OFF_TIME = int(15)              # Begin logging after 15 seconds
LOG_INTERVALS = int(10*60)              # Write a new entry every 10 mins after the initial one if the system load continues to be > MEMORY_LOAD
T_UNDER_LOAD = {'mem': 0}               # Time under load in LOG_SET_OFF_TIME//MEM_CHECK_FREQ
SET_OFF_STEP = LOG_SET_OFF_TIME//MEM_CHECK_FREQ

GENERAL_LOG_FILENAME = "general_proc_info.log"
PROC_DETAILS_FILENAME = "proc_details.log"

def get_current_time():
    '''
    Obtain current time and make it readable.
    '''
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S %d/%m/%y")
    return current_time

def get_mem_load():
    '''
    Measure memory (RSS) load.
    '''
    memory_load = psutil.virtual_memory().percent
    return memory_load

def get_proc_by_memory(num_processes=NPROC):
    '''
    Get list of running process sorted by Memory Usage.
    '''
    list_of_processes = []
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict 
           proc_info = proc.as_dict(attrs=['pid', 'name', 'username', 'cwd', 'create_time', 'status', 'cpu_percent'])
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
    return df

def get_proc_details(pid):
    '''
    An example function which can use bash commands
    to obtain more details about the process from its pid.
    '''

    ps_cmd = f"ps -Flww -p {pid}"
    proc_cmd= f"cat /proc/{pid}/status"

    ps_details  = subprocess.run(ps_cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             encoding='utf-8')
    ps_details  = ps_details.stdout

    proc_status  = subprocess.run(proc_cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             encoding='utf-8')
    proc_status = proc_status.stdout
    return ps_details, proc_status

if __name__ == '__main__':
    i = 0
    while i < 5:
        memory_load = get_mem_load()
        if memory_load > MEMORY_LOAD:
            T_UNDER_LOAD['mem'] += 1
            if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ) or (T_UNDER_LOAD['mem'] % int(LOG_INTERVALS//MEM_CHECK_FREQ)) == 0:
                proc_info = get_proc_by_memory()

                with open(os.path.join(os.getcwd(), GENERAL_LOG_FILENAME),'a') as log_file:
                    log_file.write(f"TIME: {get_current_time()}\n")
                    if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ):
                        log_file.write(f"NEW LOG\n")
                    else:
                        log_file.write(f"CURRENT LOG STARTED {((T_UNDER_LOAD['mem']*MEM_CHECK_FREQ)-LOG_SET_OFF_TIME)//60} MINUTES AGO\n")
                    log_file.write(f"{proc_info.to_string(header = True, index = True)}\n\n")
                
                with open(os.path.join(os.getcwd(), PROC_DETAILS_FILENAME),'a') as details_log_file:
                    details_log_file.write(f"TIME: {get_current_time()}\n")
                    if T_UNDER_LOAD['mem'] == int(LOG_SET_OFF_TIME//MEM_CHECK_FREQ):
                        details_log_file.write(f"NEW LOG\n")
                    else:
                        details_log_file.write(f"CURRENT LOG STARTED {((T_UNDER_LOAD['mem']*MEM_CHECK_FREQ)-LOG_SET_OFF_TIME)//60} MINUTES AGO\n")
                    for proc in list(proc_info.index.values):
                        ps_details, proc_status = get_proc_details(proc)
                        details_log_file.write(f"{ps_details}\n")
                    for proc in list(proc_info.index.values):
                        ps_details, proc_status= get_proc_details(proc)
                        details_log_file.write(f"{proc_status}\n")
        else:
            T_UNDER_LOAD['mem'] = 0
            
        time.sleep(MEM_CHECK_FREQ)
        i += 1