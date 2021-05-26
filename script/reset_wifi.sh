#!/bin/bash

cd /etc/wpa_supplicant
rm -f wpa_supplicant.conf
touch wpa_supplicant.conf
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\ncountry=US\n\nnetwork={\n        ssid="wifi"\n        psk="set"\n        key_mgmt=WPA-PSK\n        disabled=1\n}" >> wpa_supplicant.conf

