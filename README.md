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

# Setup for guest account
```
Usage command for guest account: Scripts\mitmweb.exe -s ./SPPDFilterMitmproxyAddon_GuestAccount.py

This addon tricks SPPD into using guest account,
if used on fresh SPPD installation. Allows to use SPPD normally.
This addon should be active in order to use guest account.
```

# Setup for custom card levels
```
Usage command for custom card levels: Scripts\mitmweb.exe -s ./SPPDFilterMitmproxyAddon_CustomCardLevels.py

This addon rewrites card levels and upgrades, 
allow user to open SPPD deckbuilder and explore card stats for chosen upgrade and
block every other SPPD functionality. 
```
