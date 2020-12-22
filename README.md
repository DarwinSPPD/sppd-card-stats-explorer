# sppd-card-stats-explorer
 Mitmproxy addon for changing SPPD card levels and upgrades

# Requirements 
```
This python script requires mitmproxy library. Install it with following command: Scripts\pip.exe install mitmproxy

Mitmproxy API documentation is available by using this command: python.exe -m pydoc mitmproxy

On target device change proxy to point at mitmproxy's endpoint (port 8080,
IP address == local IP adress for machine, usually comes in form 192.168.xxx.xxx),
visit internal website mitm.it and follow instructions to install certificate for SSL connection interception
```

# Latest setup
```
Usage command: Scripts\mitmdump.exe -s ./SPPDFilterMitmproxyAddon.py
```

# Setup for PVE gameplay
```
Usage command: Scripts\mitmdump.exe -s ./SPPDFilterMitmproxyAddon_Gameplay.py

To change which card should be played in PVE, refer to DEF_CUSTOM_CARD_TEST variable.
In case of need to have more than one card in the deck, change the value of DEF_CUSTOM_CARDS[0] assignment 
few rows below DEF_CUSTOM_CARD_TEST variable.
```


# Setup for card upgrades
```
Usage command: Scripts\mitmdump.exe -s ./SPPDFilterMitmproxyAddon_Upgrades.py

To change which card upgrades to show off, change DEF_CARDS_EXCLUDED_EXCEPTION variable.
```

# Setup for creating asset backup file (should become useful if South Park: Phone Destroyer servers are shut down)
```
Usage command: Scripts\mitmdump.exe -s ./SPPDFilterMitmproxyAddon_Assets.py

Currently there is no information about shutting South Park: Phone Destroyer down any time soon.
To create a backup, run this script on fresh sppd installation. About 1GB of free space is recommended.
```
