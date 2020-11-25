#!/bin/bash

# find your mic via 'pactl list short sources'
MIC_NAME='alsa_input.usb-Samson_Technologies_Samson_GoMic-00.analog-stereo'

ON_AIR_MONITOR_PID_FILE="$HOME/.on-air-monitor.pid"

if [ ! -f ${ON_AIR_MONITOR_PID_FILE} ]; then
    echo "On Air Monitor is not runnig."
    exit 1
fi

DEVICE_ID=$(pactl list short sources | grep "${MIC_NAME}" | awk '{ print $1 }')
pactl set-source-mute ${DEVICE_ID} toggle

# publish mic status
MIC_STATUS=$(pactl list sources | egrep -A999999999 "^Source #${DEVICE_ID}" | grep -m 1 'Mute:' | cut -d ':' -f 2 | xargs)

if [ $MIC_STATUS == "yes" ]; then
    kill -USR1 $(cat $ON_AIR_MONITOR_PID_FILE)
else
    kill -USR2 $(cat $ON_AIR_MONITOR_PID_FILE)
fi