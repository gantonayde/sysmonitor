SYSMONITOR_DIR=`pwd`
SERVICE_NAME='sysmonitor_test'

sudo SYSMONITOR_DIR=${SYSMONITOR_DIR} envsubst < service/sysmonitor_test.service > ${SERVICE_NAME}.service
sudo mv sysmonitor_test.service /lib/systemd/system/${SERVICE_NAME}.service
sudo chmod 644 /lib/systemd/system/${SERVICE_NAME}.service
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}.service

