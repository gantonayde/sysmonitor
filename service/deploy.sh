#!/bin/bash

SYSMONITOR_DIR=`pwd`
USERNAME=`whoami`
SERVICE_NAME='sysmonitor_example'

while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
        -r|--remove)
        REMOVE=true
        ;;
    esac
    shift
done

if [ $REMOVE ] ; then
    sudo systemctl stop ${SERVICE_NAME}.service 
    sudo rm /lib/systemd/system/${SERVICE_NAME}.service
    sudo unlink /etc/systemd/system/multi-user.target.wants/${SERVICE_NAME}.service
    sudo systemctl daemon-reload
    echo "${SERVICE_NAME}.py is removed."
else
    pip3 install -r requirements.txt 
    sudo SYSMONITOR_DIR=${SYSMONITOR_DIR} USERNAME=${USERNAME} SERVICE_NAME=${SERVICE_NAME} envsubst < service/sysmonitor_test.service > ${SERVICE_NAME}.service
    sudo mv ${SERVICE_NAME}.service /lib/systemd/system/${SERVICE_NAME}.service
    sudo chmod 644 /lib/systemd/system/${SERVICE_NAME}.service
    sudo systemctl daemon-reload
    sudo systemctl enable ${SERVICE_NAME}.service
    sudo systemctl start ${SERVICE_NAME}.service   
    echo "${SERVICE_NAME}.py installed as a service."
    echo "You can check its status with:"
    echo "sudo systemctl status ${SERVICE_NAME}.service" 
fi



