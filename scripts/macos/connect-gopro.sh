#!/bin/sh
#
# Connect to GoPro's WiFi from MacOS.
#
# Requires that you've already set up a network profile that can
# connect to the GoPro's SSID.
#
set -eu
SSID=$1
# For now assumes your wifi is on en1 because that's my setup!
INTERFACE=en1

while true
do
    echo $(date) starting gopro scan
    # see if we can find the wifi SSID
    if ! /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | fgrep -q "${SSID}"
    then
		echo "$(date) GoPro wifi SSID '${SSID}' not found - is it enabled? (sleeping 5s)"
		sleep 5
		continue
    fi

    if ifconfig "${INTERFACE}" | fgrep -q '10.5.5.'
    then
		echo "$(date) Got an address, checking for camera status"
		if curl --connect-timeout 30 http://10.5.5.9/gp/gpControl/status
		then
			break
		fi
    fi
    echo $(date)' found SSID but not connected - bouncing network'
    networksetup -setairportpower "${INTERFACE}" off
    networksetup -setairportpower "${INTERFACE}" on
    echo $(date)' pausing 20s to allow network to settle'
    sleep 20
done
