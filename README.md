# Sysmonitor example

A Python program that monitors for certain system memory and logs information about which processes use it the most if a given threshold is passed.



## File structure

The main program is the `sysmonitor_example.py`file. There are also a couple of unit test cases in `test.py`. They test if the program can read the current memory load, acquire a list of processes and execute shell commands. The full documentation is in the this file. There are two example logs in the log_examples directory. In terms of installation, the program can be installed and uninstalled with a bash script (`deploy.sh`) in the script directory. As required the program can be automatically started on every boot and run indefinitely in the background. There are two different implementations to achieve this (with `rc.local` and `systemd`). The installation process is explained below.

 
## Requirements

Python3. Libraries: `pandas` and `psutil`.

## Installation

### Automatic

Navigate into the directory where `sysmonitor_example.py` is located. Open a terminal there and type:
`./service/deploy.sh`

That should install the program along with the needed modules and create a systemd service which runs continously in the background.
Alternatively, on a RaspberryPi you can use the script with the `-rc` arguement which will edit the `/etc/rc.local` file. Then you need to reboot the system.

### Manual

You need to install the pandas and psutil modules if they are not present. Then the program can be started by running:
`python3 sysmonitor_example.py &` 

Note that the program will stop upon restart with the manual installation.

By default the program will start logging only if the memory usage is \> 80\%. You can lower the value of the `MEMORY_LOAD` variable at the top of `sysmonitor_example.py` to force things.

## Uninstall

To uninstall the service, simply pass an `-r` (for systemd install) or `-rc -r` (for rc.local install) to the script and it will remove the program. 


## How it works

The program checks the RSS memory usage (in %) every 3 seconds (arbitrary choice). If the load is above a given threshold (80% as required) and stays that way for 15 seconds the program writes a report on the system, memory usage, current time and some details for the top 5 most memory hungry processes. In another file, it gives more details about these processes like when they were created, how long they have been running, peak memory consumption, working directory, etc. If the memory load remains high the program will wait for approximately 10 mins (again an arbitrary number so the logs are not huge) before appending a new entry to the files (it will also report how long it has been since the first report). If the memory load falls below the threshold the whole process resets and any new reports will be appended with a 'new log' label.

## Tests

There are a couple of unit test cases in `test.py`. 
They test if the program can read the current memory load, acquire a list of processes and execute shell commands.
You can run the test by typing:
`python3 -m unittest -v test.py`

