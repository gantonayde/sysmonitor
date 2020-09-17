#!/bin/bash

SYSMONITOR_DIR=`pwd`
USERNAME=`whoami`
SERVICE_NAME='sysmonitor_example'
RC_LOCAL_DIR='/etc'

while [[ $# -gt 0 ]]; do
    key="$1"
    case "$key" in
        -r|--remove)
        REMOVE=true
        ;;
        -rc|--rclocal)
        RC=true
        ;;
    esac
    shift
done

if [ $REMOVE ] && ! [ $RC ] ; then
    sudo systemctl stop ${SERVICE_NAME}.service 
    sudo rm /lib/systemd/system/${SERVICE_NAME}.service
    sudo unlink /etc/systemd/system/multi-user.target.wants/${SERVICE_NAME}.service
    sudo systemctl daemon-reload
    echo "${SERVICE_NAME}.py is removed."
elif [ $RC ] && ! [ $REMOVE ]; then
    if grep -Fxq "sudo python3 ${SYSMONITOR_DIR}/${SERVICE_NAME}.py & > ${SYSMONITOR_DIR}/log.txt 2>&1" service/rc.local; then
        echo "${SERVICE_NAME}.py is already installed."
    else
        sudo sed -i "/^exit 0/i sudo python3 ${SYSMONITOR_DIR}/${SERVICE_NAME}.py & > ${SYSMONITOR_DIR}/log.txt 2>&1" ${RC_LOCAL_DIR}/rc.local
        echo "${SERVICE_NAME}.py installed. Please reboot the system."
    fi    
elif [ $RC ] && [ $REMOVE ]; then
    sudo grep -v "sudo python3 ${SYSMONITOR_DIR}/${SERVICE_NAME}.py & > ${SYSMONITOR_DIR}/log.txt 2>&1" ${RC_LOCAL_DIR}/rc.local > ${RC_LOCAL_DIR}/rc.local2;
    sudo mv ${RC_LOCAL_DIR}/rc.local2 ${RC_LOCAL_DIR}/rc.local
    echo "${SERVICE_NAME}.py removed. Please reboot the system."
else
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



