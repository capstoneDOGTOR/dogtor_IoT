
#!/bin/bash

cd /etc/wpa_supplicant
sed '/}$/a\network={\n        ssid="wifi"\n        psk="set"\n        key_mgmt=WPA-PSK\n        disabled=1\n}' wpa_supplicant.conf
