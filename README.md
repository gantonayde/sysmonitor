# Sysmonitor example

A Python program that monitors system memory and logs information about which processes use it the most.


## File structure

The main program is the `sysmonitor_example.py`file. There are also a couple of unit test cases in `test.py`. They test if the program can read the current memory usage, acquire a list of processes and execute shell commands. There are two example logs in the `example_logs` directory (1min interval between entries, 1% mem usage threshold). While running the program generates two log files (`general_proc_info.log` and `proc_details.log`) in the root directory of the project. In terms of installation, the program can be installed and uninstalled with a bash script (`deploy.sh`) located in the `script` directory. As required the program can be automatically started on every boot and run indefinitely in the background (as a `systemd` service). The installation process is explained below.

 
## Requirements

Python3. Libraries: `pandas` and `psutil` (versions are omitted on purpose).

## Installation

### Automatic

Navigate to the directory where `sysmonitor_example.py` is located, that should be the project root directory. Open a terminal there and type:
`./service/deploy.sh`

That should install the program along with the needed modules and create a systemd service which runs continously in the background.

### Manual

You need to install the pandas and psutil modules if they are not present. Then the program can be started by running:
`python3 sysmonitor_example.py &` 

Note that the program will stop upon restart with the manual installation.

By default the program will start logging only if the memory usage is \> 80\%. You can lower the value of the `MEMORY_USAGE` variable at the top of `sysmonitor_example.py` to force things.

## Uninstall

To uninstall the service, simply pass an `-r` to the script and it will remove the program, i.e.:
`./service/deploy.sh -r`


## How the program works

The program checks the RSS memory usage (in %) every 3 seconds (arbitrary choice). If the usage is above a given threshold (80% as required) and stays that way for 15 seconds the program will write a report about the system, memory usage, current time and some details for the most (top 5) memory hungry processes. In another file, it will log more details about these processes, like when they were created, how long they have been running, peak memory consumption, working directory, etc. If the memory usage remains high the program will wait for approximately 10 mins (again an arbitrary number so the logs are not huge) before appending a new entry to the files (it will also report how long it has been since the first report). If the memory usage falls below the threshold the whole process resets and any new reports will be appended with a 'new log' label.

## Tests

There are a couple of unit test cases in `test.py`. 
They test if the program can read the current memory usage, acquire a list of processes and execute shell commands.
You can run the tests by typing:
`python3 -m unittest -v test.py`

