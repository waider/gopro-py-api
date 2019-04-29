#!/bin/sh
#
# Connect to GoPro's WiFi from MacOS.
#
# Requires that you've already set up a network profile that can
# connect to the GoPro's SSID.
#
# For now assumes your wifi is on en1 because that's my setup!
#
set -eu
SSID=$1

while true
do
    echo $(date) starting gopro scan
    # see if we can find the wifi SSID
    if ! /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s | fgrep "$SSID"
    then
	echo "GoPro wifi SSID $SSID not found - is it enabled?"
	sleep 5
	continue
    fi

    if ifconfig en1 | fgrep '10.5.5.'
    then
	break
    fi
    echo 'bouncing network'
    networksetup -setairportpower en1 off
    networksetup -setairportpower en1 on
    echo 'pausing to allow setttle'
    sleep 20
done
