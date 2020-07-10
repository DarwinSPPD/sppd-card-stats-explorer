# sppd-card-stats-explorer
 Mitmproxy addon for changing SPPD card levels and upgrades

# Setup 
```This python script requires mitmproxy library. Install it with following command: Scripts\pip.exe install mitmproxy

Usage command: Scripts\mitmweb.exe -s ./SPPDFilterMitmproxyAddon.py

Mitmproxy API documentation is available by using this command: python.exe -m pydoc mitmproxy

On target device change proxy to point at mitmproxy's endpoint (port 8080,
IP address == local IP adress for machine, usually comes in form 192.168.xxx.xxx),
visit internal website mitm.it and follow instructions to install certificate for SSL connection interception
```

# Addon startup options

```If DEF_USE_CUSTOM_UPGRADE_LEVEL is [True], this addon rewrites card levels and upgrades, 
allow user to open SPPD deckbuilder and explore card stats for chosen upgrade and
block every other SPPD functionality.

If DEF_USE_CUSTOM_UPGRADE_LEVEL is [False], this addon tricks SPPD into using guest account,
if used on fresh SPPD installation. Allows to use SPPD normally.
This addon should be active in order to use guest account.
```

```Variables below DEF_UPGRADE_LEVEL, DEF_CUSTOM_CARDS, DEF_DAILY_DEAL_LOOT
only have effect if DEF_USE_CUSTOM_UPGRADE_LEVEL is set.
```

```Change DEF_UPGRADE_LEVEL variable to change levels and upgrades shown in SPPD deckbuilder
Restart of SPPD app is required after every change.

DEF_UPGRADE_LEVEL does not works with non playable cards, these cards need to loaded into a deck using
DEF_CUSTOM_CARDS variable. In order for non playable cards to show up in deck builder, these cards
need to be received from packs first. See free pack logic referenced in code.
```

```DEF_CUSTOM_CARDS loads a list of cards into sppd deck```

```DEF_DAILY_DEAL_LOOT places any item of choice in daily deal window```
