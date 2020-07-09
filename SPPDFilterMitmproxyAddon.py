## This python script requires mitmproxy library. Install it with following command: Scripts\pip.exe install mitmproxy
##
## Usage command: Scripts\mitmweb.exe -s ./SPPDFilterMitmproxyAddon.py
##
## Somewhat complete mitmproxy API documentation is available by using this command: python.exe -m pydoc mitmproxy
##
## On target device change proxy to point at mitmproxy's endpoint (port 8080,
## IP address == local IP adress for machine, usually comes in form 192.168.xxx.xxx),
## visit internal website mitm.it and follow instructions to install certificate for SSL connection interception
##
#######
##

import mitmproxy
import json
import time


##DEF_USE_CUSTOM_UPGRADE_LEVEL = [True]

## If DEF_USE_CUSTOM_UPGRADE_LEVEL is set, this addon rewrites card levels and upgrades, 
## allow user to open SPPD deckbuilder and explore card stats for chosen upgrade and
## block every other SPPD functionality.

DEF_USE_CUSTOM_UPGRADE_LEVEL = [False]

## If DEF_USE_CUSTOM_UPGRADE_LEVEL is not set, this addon tricks SPPD into using guest account,
## if used on fresh SPPD installation. Allows to use SPPD normally.
## This addon should be active in order to use guest account.

DEF_UPGRADE_LEVEL = ['lvl 1, 1/5']

## Change DEF_UPGRADE_LEVEL variable to change levels and upgrades shown in SPPD deckbuilder
## Restart of SPPD app is required after every change.

## Variable DEF_UPGRADE_LEVEL only has effect if DEF_USE_CUSTOM_UPGRADE_LEVEL is set.

## DEF_UPGRADE_LEVEL does not works with non playable cards, these cards need to loaded into a deck using
## DEF_CUSTOM_CARDS variable. In order for non playable cards to show up in deck builder, these cards
## need to be received with packs first. See free pack logic referenced in code.

DEF_CUSTOM_CARDS = [[66]]

## DEF_CUSTOM_CARDS loads a list of cards into sppd deck

upgradedict = {\
        'lvl 1, 1/5': {'s': 0, 'c': 0, 'x': 0, 'w': 1.0},\
        'lvl 1, 2/5': {'s': 0, 'c': 0, 'x': 1, 'w': 1.0},\
        'lvl 1, 3/5': {'s': 0, 'c': 0, 'x': 2, 'w': 1.0},\
        'lvl 1, 4/5': {'s': 0, 'c': 0, 'x': 3, 'w': 1.0},\
        'lvl 1, 5/5': {'s': 0, 'c': 0, 'x': 4, 'w': 1.0},\
        'lvl 2, 5/15': {'s': 1, 'c': 0, 'x': 0, 'w': 2.0},\
        'lvl 2, 6/15': {'s': 1, 'c': 0, 'x': 1, 'w': 2.0},\
        'lvl 2, 7/15': {'s': 1, 'c': 0, 'x': 2, 'w': 2.0},\
        'lvl 2, 8/15': {'s': 1, 'c': 0, 'x': 3, 'w': 2.0},\
        'lvl 2, 9/15': {'s': 1, 'c': 0, 'x': 4, 'w': 2.0},\
        'lvl 2, 10/15': {'s': 1, 'c': 0, 'x': 5, 'w': 2.0},\
        'lvl 2, 11/15': {'s': 1, 'c': 0, 'x': 6, 'w': 2.0},\
        'lvl 2, 12/15': {'s': 1, 'c': 0, 'x': 7, 'w': 2.0},\
        'lvl 2, 13/15': {'s': 1, 'c': 0, 'x': 8, 'w': 2.0},\
        'lvl 2, 14/15': {'s': 1, 'c': 0, 'x': 9, 'w': 2.0},\
        'lvl 2, 15/15': {'s': 1, 'c': 0, 'x': 10, 'w': 2.0},\
        'lvl 3, 15/25': {'s': 2, 'c': 0, 'x': 0, 'w': 3.0},\
        'lvl 3, 16/25': {'s': 2, 'c': 0, 'x': 1, 'w': 3.0},\
        'lvl 3, 17/25': {'s': 2, 'c': 0, 'x': 2, 'w': 3.0},\
        'lvl 3, 18/25': {'s': 2, 'c': 0, 'x': 3, 'w': 3.0},\
        'lvl 3, 19/25': {'s': 2, 'c': 0, 'x': 4, 'w': 3.0},\
        'lvl 3, 20/25': {'s': 2, 'c': 0, 'x': 5, 'w': 3.0},\
        'lvl 3, 21/25': {'s': 2, 'c': 0, 'x': 6, 'w': 3.0},\
        'lvl 3, 22/25': {'s': 2, 'c': 0, 'x': 7, 'w': 3.0},\
        'lvl 3, 23/25': {'s': 2, 'c': 0, 'x': 8, 'w': 3.0},\
        'lvl 3, 24/25': {'s': 2, 'c': 0, 'x': 9, 'w': 3.0},\
        'lvl 3, 25/25': {'s': 2, 'c': 0, 'x': 10, 'w': 3.0},\
        'lvl 4, 25/40': {'s': 3, 'c': 0, 'x': 0, 'w': 4.0},\
        'lvl 4, 26/40': {'s': 3, 'c': 0, 'x': 1, 'w': 4.0},\
        'lvl 4, 27/40': {'s': 3, 'c': 0, 'x': 2, 'w': 4.0},\
        'lvl 4, 28/40': {'s': 3, 'c': 0, 'x': 3, 'w': 4.0},\
        'lvl 4, 29/40': {'s': 3, 'c': 0, 'x': 4, 'w': 4.0},\
        'lvl 4, 30/40': {'s': 3, 'c': 0, 'x': 5, 'w': 4.0},\
        'lvl 4, 31/40': {'s': 3, 'c': 0, 'x': 6, 'w': 4.0},\
        'lvl 4, 32/40': {'s': 3, 'c': 0, 'x': 7, 'w': 4.0},\
        'lvl 4, 33/40': {'s': 3, 'c': 0, 'x': 8, 'w': 4.0},\
        'lvl 4, 34/40': {'s': 3, 'c': 0, 'x': 9, 'w': 4.0},\
        'lvl 4, 35/40': {'s': 3, 'c': 0, 'x': 10, 'w': 4.0},\
        'lvl 4, 36/40': {'s': 3, 'c': 0, 'x': 11, 'w': 4.0},\
        'lvl 4, 37/40': {'s': 3, 'c': 0, 'x': 12, 'w': 4.0},\
        'lvl 4, 38/40': {'s': 3, 'c': 0, 'x': 13, 'w': 4.0},\
        'lvl 4, 39/40': {'s': 3, 'c': 0, 'x': 14, 'w': 4.0},\
        'lvl 4, 40/40': {'s': 3, 'c': 0, 'x': 15, 'w': 4.0},\
        'lvl 5, 40/55': {'s': 4, 'c': 0, 'x': 0, 'w': 5.0},\
        'lvl 5, 41/55': {'s': 4, 'c': 0, 'x': 1, 'w': 5.0},\
        'lvl 5, 42/55': {'s': 4, 'c': 0, 'x': 2, 'w': 5.0},\
        'lvl 5, 43/55': {'s': 4, 'c': 0, 'x': 3, 'w': 5.0},\
        'lvl 5, 44/55': {'s': 4, 'c': 0, 'x': 4, 'w': 5.0},\
        'lvl 5, 45/55': {'s': 4, 'c': 0, 'x': 5, 'w': 5.0},\
        'lvl 5, 46/55': {'s': 4, 'c': 0, 'x': 6, 'w': 5.0},\
        'lvl 5, 47/55': {'s': 4, 'c': 0, 'x': 7, 'w': 5.0},\
        'lvl 5, 48/55': {'s': 4, 'c': 0, 'x': 8, 'w': 5.0},\
        'lvl 5, 49/55': {'s': 4, 'c': 0, 'x': 9, 'w': 5.0},\
        'lvl 5, 50/55': {'s': 4, 'c': 0, 'x': 10, 'w': 5.0},\
        'lvl 5, 51/55': {'s': 4, 'c': 0, 'x': 11, 'w': 5.0},\
        'lvl 5, 52/55': {'s': 4, 'c': 0, 'x': 12, 'w': 5.0},\
        'lvl 5, 53/55': {'s': 4, 'c': 0, 'x': 13, 'w': 5.0},\
        'lvl 5, 54/55': {'s': 4, 'c': 0, 'x': 14, 'w': 5.0},\
        'lvl 5, 55/55': {'s': 4, 'c': 0, 'x': 15, 'w': 5.0},\
        'lvl 6, 55/70': {'s': 5, 'c': 0, 'x': 0, 'w': 7.0},\
        'lvl 6, 56/70': {'s': 5, 'c': 0, 'x': 1, 'w': 7.0},\
        'lvl 6, 57/70': {'s': 5, 'c': 0, 'x': 2, 'w': 7.0},\
        'lvl 6, 58/70': {'s': 5, 'c': 0, 'x': 3, 'w': 7.0},\
        'lvl 6, 59/70': {'s': 5, 'c': 0, 'x': 4, 'w': 7.0},\
        'lvl 6, 60/70': {'s': 5, 'c': 0, 'x': 5, 'w': 7.0},\
        'lvl 6, 61/70': {'s': 5, 'c': 0, 'x': 6, 'w': 7.0},\
        'lvl 6, 62/70': {'s': 5, 'c': 0, 'x': 7, 'w': 7.0},\
        'lvl 6, 63/70': {'s': 5, 'c': 0, 'x': 8, 'w': 7.0},\
        'lvl 6, 64/70': {'s': 5, 'c': 0, 'x': 9, 'w': 7.0},\
        'lvl 6, 65/70': {'s': 5, 'c': 0, 'x': 10, 'w': 7.0},\
        'lvl 6, 66/70': {'s': 5, 'c': 0, 'x': 11, 'w': 7.0},\
        'lvl 6, 67/70': {'s': 5, 'c': 0, 'x': 12, 'w': 7.0},\
        'lvl 6, 68/70': {'s': 5, 'c': 0, 'x': 13, 'w': 7.0},\
        'lvl 6, 69/70': {'s': 5, 'c': 0, 'x': 14, 'w': 7.0},\
        'lvl 6, 70/70': {'s': 5, 'c': 0, 'x': 15, 'w': 7.0},\
        'lvl 7, 70/70': {'s': 6, 'c': 0, 'x': 0, 'w': 7.0},\
        '0': {'s': 0, 'c': 0, 'x': 0, 'w': 1.0}}

CharacterNames = {\
        1701: b'Calamity Heidi', \
        1700: b'Bandita Sally', \
        131: b'Smuggler Ike', \
        140: b'Captain Wendy', \
        27: b'Deckhand Butters', \
        35: b'Gunslinger Kyle', \
        50: b'Hookhand Clyde', \
        92: b'Pirate Ship Timmy', \
        200: b'Shaman Token', \
        2114: b'Sharpshooter Shelly', \
        205: b'Storyteller Jimmy', \
        1276: b'Arrowstorm', \
        1288: b'Barrel Dougie', \
        1808: b'Buccaneer Bebe', \
        134: b'Inuit Kenny', \
        186: b'Lightning Bolt', \
        28: b'Outlaw Tweek', \
        8: b'Medicine Woman Sharon', \
        45: b'Sheriff Cartman', \
        12: b'Stan of Many Moons', \
        2044: b'Swashbuckler Red', \
        2266: b'Thunderbird', \
        2209: b'Big Mesquite Murph', \
        48: b'Incan Craig', \
        10: b'Pocahontas Randy', \
        24: b'Fireball', \
        2013: b'Swordsman Garrison', \
        55: b'Astronaut Butters', \
        209: b'Enforcer Jimmy', \
        203: b'Space Warrior Token', \
        193: b'Alien Clyde', \
        1949: b'Bounty Hunter Kyle', \
        1824: b'Four-Assed Monkey', \
        40: b'Freeze Ray', \
        133: b'Gizmo Ike', \
        52: b'Ice Sniper Wendy', \
        1657: b'Poison', \
        30: b'Program Stan', \
        1805: b'Robo Bebe', \
        2308: b'Space Pilot Bradley', \
        1813: b'Visitors', \
        46: b'Warboy Tweek', \
        2101: b'Alien Drone', \
        146: b'Cyborg Kenny', \
        1269: b'Hyperdrive', \
        49: b'Marine Craig', \
        88: b'Mecha Timmy', \
        1272: b'Mind Control', \
        1311: b'Powerfist Dougie', \
        2251: b'Sizzler Stuart', \
        1509: b'Alien Queen Red', \
        38: b'A.W.E.S.O.M.-O 4000', \
        137: b'Sixth Element Randy', \
        84: b'Choirboy Butters', \
        1286: b'Power Bind', \
        1273: b'Purify', \
        86: b'Angel Wendy', \
        1923: b'Cupid Cartman', \
        2299: b'Dark Angel Red', \
        208: b'Friar Jimmy', \
        51: b'Hercules Clyde', \
        138: b'Hermes Kenny', \
        31: b'Poseidon Stan', \
        1277: b'Regeneration', \
        132: b'Scout Ike', \
        1218: b'Youth Pastor Craig', \
        158: b'Zen Cartman', \
        1307: b'Energy Staff', \
        85: b'Hallelujah', \
        1983: b'Imp Tweek', \
        2217: b'Jesus', \
        1804: b'Medusa Bebe', \
        1504: b'Prophet Dougie', \
        1216: b'The Master Ninjew', \
        201: b'Witch Doctor Token', \
        44: b'Sexy Nun Randy', \
        1274: b'Unholy Combustion', \
        87: b'Pope Timmy', \
        2043: b'Priest Maxi', \
        57: b'Paladin Butters', \
        37: b'Princess Kenny', \
        1686: b'Underpants Gnomes', \
        1806: b'Blood Elf Bebe', \
        144: b'Canadian Knight Ike', \
        91: b'Catapult Timmy', \
        61: b'Dark Mage Craig', \
        2042: b'Elven King Bradley', \
        141: b'Shieldmaiden Wendy', \
        29: b'Stan the Great', \
        1656: b'Chicken Coop', \
        2295: b'City Wok Guy', \
        1972: b'Dragonslayer Red', \
        1506: b'Dwarf Engineer Dougie', \
        179: b'Dwarf King Clyde', \
        89: b'Kyle of the Drow Elves', \
        206: b'Le Bard Jimmy', \
        47: b'Robin Tweek', \
        54: b'Rogue Token', \
        135: b'The Amazingly Randy', \
        176: b'Witch Garrison', \
        2035: b'Mr. Slave Executioner', \
        2210: b'Sorceress Liane', \
        1655: b'Transmogrify', \
        1472: b'Cock Magic', \
        32: b'Grand Wizard Cartman', \
        2200: b'Captain Diabetes', \
        2316: b'Chaos Hamsters', \
        2117: b'Super Fart', \
        2130: b'The Chomper', \
        2132: b'Fastpass', \
        2190: b'Lava!', \
        2091: b'Mosquito', \
        2202: b'Professor Chaos', \
        2262: b'Super Craig', \
        2144: b'Toolshed', \
        2195: b'Doctor Timothy', \
        2290: b'General Disarray', \
        2143: b'Human Kite', \
        2216: b'Mintberry Crunch', \
        2098: b'Tupperware', \
        2261: b'Wonder Tweek', \
        2147: b'Mysterion', \
        2141: b'The Coon', \
        2136: b'Call Girl', \
        1674: b'DogPoo', \
        1872: b'Mr. Hankey', \
        1666: b'Nelly', \
        1407: b'Rat Swarm', \
        1947: b'Towelie', \
        1869: b'Marcus', \
        2258: b'Mayor McDaniels', \
        2074: b'Mr Mackey', \
        15: b'Nathan', \
        1886: b'PC Principal', \
        1684: b'Pigeon Gang', \
        1670: b'Starvin\' Marvin', \
        1680: b'Terrance and Phillip', \
        1665: b'Terrance Mephesto', \
        1682: b'Big Gay Al', \
        1973: b'Classi', \
        1661: b'Mimsy', \
        2030: b'President Garrison', \
        2081: b'Santa Claus', \
        1683: b'Officer Barbrady', \
        2080: b'Satan', \
        1672: b'ManBearPig'}

class SPPDFilter:


        def request(self, flow):
##                #returns Request(POST android.googleapis.com:443/auth/devicekey)
##                mitmproxy.ctx.log.info('type(flow.request) == ' + repr(type(flow.request)))
##
##                #returns <class 'mitmproxy.http.HTTPRequest'>
##                mitmproxy.ctx.log.info('flow.request == ' + repr(flow.request))

                #
                
##                mitmproxy.ctx.log.info('flow.reply == ' + repr(flow.reply))
                while True:
                        if flow.request.url == 'https://android.googleapis.com/auth':
                                break
##                        if flow.request.url.startswith('https://app-measurement.com/'):
##                                break
##                        if flow.request.url == 'https://reports.crashlytics.com/spi/v1/platforms/android/apps/com.ubisoft.dragonfire/reports':
##                                break
                        if flow.request.url == 'https://connectivitycheck.gstatic.com/generate_204':
                                break
##                        if flow.request.url == 'https://launches.appsflyer.com/api/v5.2/androidevent?app_id=com.ubisoft.dragonfire&buildnumber=5.2.0':
##                                break
##                        if flow.request.url == 'https://android.clients.google.com/c2dm/register3':
##                                break
##                        if flow.request.url == 'https://www.googleapis.com/games/v1/applications/played':
##                                break
##                        if flow.request.url == 'https://www.googleapis.com/games/v1/events?language=en-US':
##                                break
##                        if flow.request.url == 'https://www.googleapis.com/games/v1/achievements?language=en-US':
##                                break
##                        if flow.request.url.startswith('https://www.googleapis.com/games/v1/players/'):
##                                break
                        if flow.request.url == 'https://play.googleapis.com/play/log/timestamp':
                                break
##                        if flow.request.url == 'https://play.googleapis.com/play/log?format=raw&proto_v2=true':
##                                break
##                        if flow.request.url == 'https://android.googleapis.com/auth/devicekey':
##                                break
                        if flow.request.url == 'https://public-ubiservices.ubi.com/v3/profiles/sessions':
                                break
##                        if flow.request.url == 'https://ssl.google-analytics.com/batch':
##                                break
                        if flow.request.url == 'https://msr-public-ubiservices.ubi.com/v1/spaces/news?spaceId=1a49a190-9703-4460-91fc-f17c4314ecc3':
                                break
##                        if flow.request.url.startswith('https://gamecfg-mob.ubi.com/profile/?action=register&productid=682'):
##                                break
                        if flow.request.url.startswith('https://ubistatic-a.akamaihd.net/0081/'):
                                break
##                        if flow.request.url.startswith('https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/'):
##                                break
##                        if flow.request.url.startswith('https://ubistatic-a.akamaihd.net/0081/stable/726560_2_a759a44bc098309da118e838391d356e/'):
##                                break
                        if flow.request.url == 'https://public-ubiservices.ubi.com/v1/applications/b5f1619b-8612-4966-a083-2fac253e2090/configuration':
                                break
##                        if flow.request.url.startswith('https://msr-public-ubiservices.ubi.com/v2/spaces/1a49a190-9703-4460-91fc-f17c4314ecc3/'):
##                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/version':
                                break
##                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/gamestate/call_outs/NewSHMaterials':
##                                break
                        if flow.request.url == 'https://msr-public-ubiservices.ubi.com/v2/spaces/1a49a190-9703-4460-91fc-f17c4314ecc3/configs/events':
                                break
##                        if flow.request.url.startswith('https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/store/catalogs?id=7,8,9,10,11,12&'):
##                                break
                        if flow.request.url.startswith('https://img.youtube.com/'):
                                break
##                        if flow.request.url == 'https://android.clients.google.com/fdfe/skuDetails':
##                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/profiles/ubimobile':
                                break
##                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/gamestate/entries':
##                                break
##                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/achievement/status':
##                                break
##                        if flow.request.url == 'https://android.clients.google.com/fdfe/ees/bulkAcquire?nocache_qos=lt':
##                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/start':
                                break
                        if flow.request.url.startswith('http://mitm.it/'):
                                break
                        if flow.request.url.startswith('https://android.clients.google.com/fdfe/apps/checkLicense?pkgn=com.ubisoft.dragonfire'):
                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/profiles/names':
                                break
                        if DEF_USE_CUSTOM_UPGRADE_LEVEL[0] == False:
                                if flow.request.url.startswith('https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/'):
                                        break
                                if flow.request.url.startswith('https://msr-public-ubiservices.ubi.com/v2/profiles/'):
                                        break
                        if DEF_USE_CUSTOM_UPGRADE_LEVEL[0] == True:















# Free pack logic here

                                if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/cardpack/cardpacks/free':
                                        debug_time_start = time.time()
##                                        cards_field_i = 2
                                        cards_field = [{"id": 1407,"quantity": 0}]
##                                        while cards_field_i <= 2:
##                                                cards_field.append({"id": cards_field_i,"quantity": 1})
##                                                cards_field_i += 1
                                        gear_field = []
##                                        gear_field_i = 153
##                                        while gear_field_i <= 153:
##                                                gear_field.append({"id": gear_field_i})
##                                                gear_field_i += 1
                                        flow.response = mitmproxy.http.HTTPResponse.make(200, \
                                                                                         json.dumps({"contents": {"balance": [],\
                                                                                                                  "cards": cards_field,\
                                                                                                                  "gear": gear_field,\
                                                                                                                  "items": []},\
                                                                                                     "next_timestamp": int(time.time())}).encode())
                                        mitmproxy.ctx.log.info('custom response flow.request.url == ' + repr(flow.request.url))
##                                        mitmproxy.ctx.log.info('custom response took ' + str((time.time() - debug_time_start)) + ' seconds')
                                        break
                                if flow.request.url.startswith('https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/techtree/cards/') and \
                                   (flow.request.url.endswith('/evolve') or flow.request.url.endswith('/upgrade')):
                                        
                                        flow.response = mitmproxy.http.HTTPResponse.make(200, \
                                                                                         json.dumps({}).encode())
                                        mitmproxy.ctx.log.info('custom response flow.request.url == ' + repr(flow.request.url))
                                        break
                                                               

                        # gear
                        # 153 - MISSING:DF_NAME_NAKEDSHIRT
                        # 155 - Cowboy Hat
                        # 180 - Knight Outfit
                        # 181 - Pope Hat
                        # 194 - Astronaut Suit
                        # 195 - Astronaut Helmet
                        # 196 - Pope Robe
                        # 198 - Knight Helmet
                        # 204 - Cowboy Shirt
                        # 1256 - Indian Tunic
                        # 1267 - Pirate Bandana
                        # 1268 - Pirate Shirt
                        # 1283 - Cyborg Outfit
                        # 1285 - Cyborg Mask
                        # 1290 - Ninja Outfit
                        # 1291 - Ninja Mask
                        # 1293 - Genie Hat
                        # 1294 - Genie Costume
                        # 1302 - Dwarf Outfit
                        # 1303 - Dwarf Helmet
                        # 1336 - Alien Costume
                        # 1337 - Alien Hat
                        # 1341 - Goth Shirt
                        # 1540-1555 - ??? Card does not open, can't navigate away from pack, animations are still working
                        # 1556 - MISSING:DF_NAME_NAKEDLADY
                        # 1558 - ??? 
                        # 1560-1562 - ??? 
                        # 1564-1566 - ??? 
                        # 1568-1621 - ??? 
                        # 1623-1628 - ???
                        # 1635 - ???
                        # 1639-1640 - ???
                        # 1668-1669 - ???
                        # 1733 - MISSING:DF_NAME_ADVENTURECOWBOY2SHIRT
                        # 1734 - MISSING:DF_NAME_ADVENTURECOWBOY2HAT
                        # 1743 - Dwarf Girl Hat
                        # 1744 - Dwarf Girl Costume
                        # 1746 - Greek God Shirt
                        # 1747 - Greek God Hat
                        # 1749 - Fairy Hat
                        # 1750 - Fairy Costume
                        # 1752 - Witch Hat
                        # 1753 - Witch Costume
                        # 1755 - Robot Mask
                        # 1756 - Robot Costume
                        # 1757 - Bear Hat
                        # 1758 - Bear Costume
                        # 1764 - Monk Shirt
                        # 1765 - Virgin Mary Hat
                        # 1766 - Virgin Mary Shirt
                        # 1768-1803 - ???
                        # 1811 - Greek Shirt
                        # 1812 - Greek Hat
                        # 1814 - Thug Hat
                        # 1815 - Thug Shirt
                        # 1816 - Luchador Mask
                        # 1817 - Luchador Costume
                        # 1818 - Butch Shirt
                        # 1827 - Manbearpig Mask
                        # 1828 - Manbearpig Costume
                        # 1830 - Futuristic Costume
                        # 1831 - Futuristic Helmet
                        # 1835 - MISSING:DF_NAME_NEUTRALBUTCHHAT
                        # 1848 - MISSING:DF_NAME_FANTASYELFGIRLHAT
                        # 1849 - MISSING:DF_NAME_FANTASYELFGIRLSHIRT
                        # 1850 - Hazmat Headgear
                        # 1851 - Hazmat Suit
                        # 1853 - Bandito Hat
                        # 1854 - Bandito Shirt
                        # 1855 - Cowboy Hat
                        # 1856 - Cowboy Shirt
                        # 1857 - Crusader Hat
                        # 1858 - Crusader Shirt
                        # 1859 - Wizard Hat
                        # 1860 - Wizard Robe
                        # 1861 - Dark Priest Hat
                        # 1862 - Dark Priest Outfit
                        # 1863 - MISSING:DF_NAME_ADVENTURECOWGIRL2HAT
                        # 1864 - MISSING:DF_NAME_ADVENTURECOWGIRL2SHIRT
                        # 1865 - Alien Hat
                        # 1866 - Alien Costume
                        # 1867 - MISSING:DF_NAME_FANASYKNIGHTBRUSHHAT
                        # 1876 - Captain's Hat
                        # 1877 - Captain's Coat
                        # 1878 - Dragon Hat
                        # 1879 - Dragon Costume
                        # 1880 - Lab Coat
                        # 1882 - Lab Glasses
                        # 1883 - Waterbear Hat
                        # 1884 - Waterbear Costume
                        # 1892 - ???
                        # 1896 - ???
                        # 1897 - PC Polo
                        # 1899 - Santa Hat
                        # 1900 - Christmas Jersey
                        # 1902 - Christmas Elf Hat
                        # 1903 - Christmas Elf Shirt
                        # 1905 - MISSING:DF_NAME_NEUTRALHOGMANAYKILTSHI
                        # 1906 - Christmas Hat
                        # 1907 - Winter Jersey
                        # 1912 - ???
                        # 1915 - Reindeer Hat
                        # 1916 - Santa's Stocking Jersey
                        # 1917 - ???
                        # 1919 - Medusa Hat
                        # 1920 - Medusa Shirt
                        # 1921 - Priest Hat
                        # 1922 - Priest Shirt
                        # 1930 - Cupid Arrow Hat
                        # 1931 - Cupid Costume
                        # 1932 - Heart Dress
                        # 1934 - Heart Suit
                        # 1936 - Pajamas
                        # 1937 - Terrance Shirt
                        # 1938 - Phillip Shirt
                        # 1939 - T&P Shirt
                        # 1944 - Galactic Titan Hat
                        # 1945 - Galactic Titan Shirt
                        # 1951 - Rubber Ducky
                        # 1952 - Towel
                        # 1954 - I Hate Towelie T-Shirt
                        # 1955 - I Love Towelie T-Shirt
                        # 1961 - Propeller Hat
                        # 1967 - Peruvian Hat
                        # 1968 - Peruvian Clothes
                        # 1969 - Spaceship Hat
                        # 1970 - Spaceship Costume
                        # 1976 - MISSING:DF_NAME_NEUTRALCLASSISHIRT
                        # 1979 - Space Dude Hat
                        # 1980 - Space Dude Shirt
                        # 1985 - Firecracker Hat
                        # 1986 - Firecracker Costume
                        # 1987 - Elf Hat
                        # 1988 - Elf Shirt
                        # 2009 - Voodoo Priest Hat
                        # 2010 - Voodoo Priest Shirt
                        # 2011 - Barbarian Hat
                        # 2012 - Barbarian Shirt
                        # 2021 - Cosmic Hat
                        # 2022 - Cosmic Shirt
                        # 2027 - MISSING:DF_NAME_FANTASYFAUNHAT
                        # 2031 - Popcorn Hat
                        # 2032 - Popcorn Shirt
                        # 2038 - Jersey
                        # 2039 - Leather Jacket
                        # 2046 - Party Hat
                        # 2047 - Program Hat
                        # 2048 - Program Shirt
                        # 2049 - Halloween Shirt
                        # 2050 - Halloween Hat
                        # 2051 - Sailor Hat
                        # 2055 - Masquerade Hat
                        # 2057 - Masquerade Costume
                        # 2059 - Hemp Hat
                        # 2060 - Hemp Shirt
                        # 2061 - Samurai Hat
                        # 2062 - Samurai Costume
                        # 2063 - Pinata Hat
                        # 2064 - Pinata Costume
                        # 2067 - Jester Shirt
                        # 2070 - Jester Hat
                        # 2072 - Explorer Hat
                        # 2073 - Explorer Shirt
                        # 2075 - Hockey Mask
                        # 2076 - Mummy Mask
                        # 2077 - Mummy Shirt
                        # 2082 - Crown
                        # 2083 - Ritual Hat
                        # 2084 - Ritual Shirt
                        # 2085 - Clown Hat
                        # 2086 - Clown Costume
                        # 2087 - Cloak and Medal
                        # 2088 - Test Dummy Hat
                        # 2089 - Test Dummy Shirt
                        # 2090 - Xmas Shirt
                        # 2094 - Box Hat
                        # 2100 - Safety Vest
                        # 2103 - Tiara
                        # 2104 - Feather Shirt
                        # 2105 - Gladiator Hat
                        # 2106 - Gladiator Shirt
                        # 2107 - Roman Gladiator Hat
                        # 2108 - Roman Gladiator Shirt
                        # 2138 - Supergirl Shirt
                        # 2139 - Dr Bad Shirt
                        # 2150 - Bucket Basher Hat
                        # 2151 - Bucket Basher Shirt
                        # 2154 - Hot Stuff Hat
                        # 2155 - Hot Stuff Shirt
                        # 2173-2174 - ???
                        # 2211 - MISSING:DF_NAME_CRATESOAPBOXDEFAULT
                        # 2212 - Golden Box
                        # 2218 - Shirt
                        # 2219 - Hat
                        # 2226 - Tegridy Hat
                        # 2227 - Tegridy Shirt
                        # 2228 - Fingerbang Hat
                        # 2229 - Fingerbang Shirt
                        # 2231 - Battle Tested
                        # 2232 - 300 Fingerbang Hat
                        # 2233 - 300 Fingerbang Shirt
                        # 2235 - Goo Man Hat
                        # 2236 - Goo Man Shirt
                        # 2239 - Archaeologist Hat
                        # 2240 - Archaeologist Shirt
                        # 2241 - Scary Pajamas
                        # 2243 - Christmas Tree Hat
                        # 2244 - Christmas Tree Shirt
                        # 2246 - Strong Woman Hat
                        # 2247 - Strong Woman Shirt
                        # 2250 - Christmas Gift
                        # 2253 - Turd Hat
                        # 2255 - Turd Shirt
                        # 2256 - Cable Guy Shirt
                        # 2259 - Snowman Hat
                        # 2260 - Snowman Shirt
                        # 2273 - Tegridy Box
                        # 2280 - Love Box
                        # 2288 - Captain Cosmos Hat
                        # 2289 - Captain Cosmos Shirt
                        # 2292 - Doom Device Box
                        # 2293 - Bunny Shirt
                        # 2294 - Bunny Hat
                        # 2303 - Brainiac Shirt
                        # 2304 - Brainiac Hat
                        # 2306 - Robot Box
                        # 2314 - Dark Angel Shirt
                        # 2315 - Dark Angel Hat
                        # 2320 - Chaos Minion #42 Hat
                        # 2321 - Chaos Minion #42 Shirt
                        
                        
                        
                        
                        
                        
                        # cards
                        # 1 - Interrupts reading deck information, freezes free pack animation and the game
                        #8: b'Medicine Woman Sharon', \
                        #10: b'Pocahontas Randy', \
                        #12: b'Stan of Many Moons', \
                        # 13 - Mimsy
                        # 14 - Stan of Many Moons
                        #15: b'Nathan', \
                        # 16 - Sheriff Cartman
                        # 20 - Sheriff Cartman
                        # 23 - Stan of Many Moons
                        #24: b'Fireball', \
                        #27: b'Deckhand Butters', \
                        #28: b'Outlaw Tweek', \
                        #29: b'Stan the Great', \
                        #30: b'Program Stan', \
                        #31: b'Poseidon Stan', \
                        #32: b'Grand Wizard Cartman', \
                        # 33 - Indian Hunter
                        # 34 - Indian Brave
                        #35: b'Gunslinger Kyle', \
                        # 36 - Bounty Hunter Kyle
                        #37: b'Princess Kenny', \
                        #38: b'A.W.E.S.O.M.-O 4000', \
                        # 39 - Little Choirboy
                        #40: b'Freeze Ray', \
                        #44: b'Sexy Nun Randy', \
                        #45: b'Sheriff Cartman', \
                        #46: b'Warboy Tweek', \
                        #47: b'Robin Tweek', \
                        #48: b'Incan Craig', \
                        #49: b'Marine Craig', \
                        #50: b'Hookhand Clyde', \
                        #51: b'Hercules Clyde', \
                        #52: b'Ice Sniper Wendy', \
                        #54: b'Rogue Token', \
                        #55: b'Astronaut Butters', \
                        # 56 - Pocahontas Randy
                        #57: b'Paladin Butters', \
                        # 59 - ??? (Tank, Neutral, Common)
                        # 60 - Sheriff Cartman
                        #61: b'Dark Mage Craig', \
                        # 62 - ??? (Tank, Neutral, Common)
                        # 63 - Stan of Many Moons
                        # 64 - ??? (Tank, Neutral, Common)
                        # 65 - Poseidon Stan
                        # 66 - ??? (Ranged, Fantasy, Rare)
                        # 67 - Paladin Butters
                        # 68 - Rogue Token
                        # 69 - MISSING:DF_NAME_KENNYGEN
                        # 70 - Deckhand Butters
                        # 71 - Stan the Great
                        # 72 - MISSING:DF_NAME_TWEEKGEN
                        # 73 - Program Stan
                        # 75 - Grand Wizard Cartman
                        # 76 - Astronaut Butters
                        # 77 - Nathan
                        # 78 - Mimsy
                        # 79 - Pocahontas Randy
                        # 80 - Medicine Woman Sharon
                        #84: b'Choirboy Butters', \
                        #85: b'Hallelujah', \
                        #86: b'Angel Wendy', \
                        #87: b'Pope Timmy', \
                        #88: b'Mecha Timmy', \
                        #89: b'Kyle of the Drow Elves', \
                        #91: b'Catapult Timmy', \
                        #92: b'Pirate Ship Timmy', \
                        #131: b'Smuggler Ike', \
                        #132: b'Scout Ike', \
                        #133: b'Gizmo Ike', \
                        #134: b'Inuit Kenny', \
                        #135: b'The Amazingly Randy', \
                        #137: b'Sixth Element Randy', \
                        #138: b'Hermes Kenny', \
                        #140: b'Captain Wendy', \
                        #141: b'Shieldmaiden Wendy', \
                        # 143 - Imp Tweek
                        #144: b'Canadian Knight Ike', \
                        #146: b'Cyborg Kenny', \
                        #158: b'Zen Cartman', \
                        #176: b'Witch Garrison', \
                        #179: b'Dwarf King Clyde', \
                        # 182 - Gizmo Ike
                        # 184 - Gizmo Ike
                        # 185 - Gizmo Ike
                        #186: b'Lightning Bolt', \
                        #193: b'Alien Clyde', \
                        #200: b'Shaman Token', \
                        #201: b'Witch Doctor Token', \
                        #203: b'Space Warrior Token', \
                        #205: b'Storyteller Jimmy', \
                        #206: b'Le Bard Jimmy', \
                        #208: b'Friar Jimmy', \
                        #209: b'Enforcer Jimmy', \
                        #1216: b'The Master Ninjew', \
                        #1218: b'Youth Pastor Craig', \
                        #1269: b'Hyperdrive', \
                        #1272: b'Mind Control', \
                        #1273: b'Purify', \
                        #1274: b'Unholy Combustion', \
                        #1276: b'Arrowstorm', \
                        #1277: b'Regeneration', \
                        # 1278 - MISSING:DF_NAME_SPELLDARKRESURRECT
                        #1286: b'Power Bind', \
                        #1288: b'Barrel Dougie', \
                        # 1298 - Arrow Tower
                        #1307: b'Energy Staff', \
                        #1311: b'Powerfist Dougie', \
                        # 1319 - Inuit Kenny
                        # 1320 - Gunslinger Kyle
                        # 1321 - Sheriff Cartman
                        # 1324 - Medicine Woman Sharon
                        # 1331 - Indian Brute
                        # 1404 - A Rat
                        # 1405 - A Rat
                        # 1406 - A Rat
                        #1407: b'Rat Swarm', \
                        # 1423 - Cyborg Kenny
                        # 1426 - Space Grunt
                        # 1427 - Space Gunner
                        # 1428 - Cyborg Titan
                        # 1434 - Gizmo Ike
                        # 1435 - Cyborg Kenny
                        # 1437 - Enforcer Jimmy
                        # 1439 - Ice Sniper Wendy
                        # 1440 - Mecha Timmy
                        # 1441 - Indian Brave
                        # 1442 - Alien Clyde
                        # 1444 - Gizmo Ike
                        # 1445 - MISSING:DF_NAME_SPELLRATATTACKFAN
                        # 1446 - A Rat
                        # 1447 - A Rat
                        # 1448 - A Rat
                        # 1449 - Cyborg Kenny
                        # 1451 - Enforcer Jimmy
                        # 1453 - Program Stan
                        # 1454 - Powerfist Dougie
                        # 1455 - Ice Sniper Wendy
                        # 1456 - A Cock
                        # 1470 - Arrow Tower
                        ##1472: b'Cock Magic', \
                        # 1473 - Storyteller Jimmy
                        # 1474 - Captain Wendy
                        # 1484 - Barrel Dougie
                        # 1485 - Hookhand Clyde
                        ##1504: b'Prophet Dougie', \
                        ##1506: b'Dwarf Engineer Dougie', \
                        ##1509: b'Alien Queen Red', \
                        # 1512 - Choirboy Butters
                        # 1513 - Scout Ike
                        # 1514 - Hermes Kenny
                        # 1515 - Angel Wendy
                        # 1516 - Friar Jimmy
                        # 1517 - Witch Doctor Token
                        # 1518 - The Master Ninjew
                        # 1519 - Sexy Nun Randy
                        # 1520 - Pope Timmy
                        # 1521 - Robin Tweek
                        # 1522 - Canadian Knight Ike
                        # 1523 - Kyle of the Drow Elves
                        # 1524 - Catapult Timmy
                        # 1525 - The Amazingly Randy
                        # 1526 - Stan the Great
                        # 1527 - Dwarf King Clyde
                        # 1528 - Dark Mage Craig
                        # 1529 - Le Bard Jimmy
                        # 1530 - Rogue Token
                        # 1531 - Grand Wizard Cartman
                        # 1532 - Princess Kenny
                        # 1533 - Zionist Ranger
                        # 1631 - Pirate Ship Timmy
                        # 1641 - Space Assasin
                        # 1644 - Little Choirboy
                        # 1645 - Mormon Missionary
                        # 1647 - Subzero Titan
                        # 1649 - Royal Archer
                        # 1650 - Turbo Space Grunt
                        # 1651 - Royal Archer
                        # 1652 - Tank Kid
                        # 1653 - Indian Warrior
                        ##1655: b'Transmogrify', \
                        ##1656: b'Chicken Coop', \
                        ##1657: b'Poison', \
                        # 1658 - Beast Mode
                        # 1659 - Invincibility
                        ##1661: b'Mimsy', \
                        # 1664 - MISSING:MR GNOME
                        ##1665: b'Terrance Mephesto', \
                        ##1666: b'Nelly', \
                        # 1667 - MISSING:GROSS PIDGEON
                        ##1670: b'Starvin\' Marvin', \
                        ##1672: b'ManBearPig'}
                        ##1674: b'DogPoo', \
                        ##1680: b'Terrance and Phillip', \
                        ##1682: b'Big Gay Al', \
                        ##1683: b'Officer Barbrady', \
                        ##1684: b'Pigeon Gang', \
                        # 1685 - Pidgeons
                        ##1686: b'Underpants Gnomes', \
                        # 1688 - Healing Fountain
                        # 1689 - Toxic Pylon
                        # 1690 - Rune Totem
                        # 1691 - Cyborg Tower
                        # 1692 - Shaman Token
                        # 1693 - Alien Queen Red
                        # 1694 - Space Warrior Token
                        # 1695 - Sixth Element Randy
                        # 1696 - Marine Craig
                        # 1698 - Bounty Hunter Kyle
                        ##1700: b'Bandita Sally', \
                        ##1701: b'Calamity Heidi', \
                        # 1702 - Auto-Vacuum
                        # 1703 - Incan Craig
                        # 1704 - Imp Tweek
                        # 1705 - Holy Defender
                        # 1708 - Prophet Dougie
                        # 1715 - Castle Defender
                        # 1716 - Squire
                        # 1717 - Native Hunter
                        # 1718 - Crusader
                        # 1719 - Arrowstorm Caster
                        # 1720 - Lightning Bolt Caster
                        # 1723 - Dwarf Engineer Dougie
                        # 1724 - Youth Pastor Craig
                        # 1725 - Shieldmaiden Wendy
                        # 1726 - Stan the Great
                        # 1727 - Indian Brute
                        # 1728 - Subzero Titan
                        # 1735 - Mormon Missionary
                        # 1736 - Witch Doctor Token
                        # 1737 - Shieldmaiden Wendy
                        # 1738 - Imp Tweek
                        # 1740 - Smuggler Ike
                        ##1804: b'Medusa Bebe', \
                        ##1805: b'Robo Bebe', \
                        ##1806: b'Blood Elf Bebe', \
                        ##1808: b'Buccaneer Bebe', \
                        ##1813: b'Visitors', \
                        # 1820 - Snake
                        ##1824: b'Four-Assed Monkey', \
                        # 1841 - Terrance and Phillip
                        # 1843 - Underpants Gnomes
                        # 1845 - A Rat
                        ##1869: b'Marcus', \
                        # 1870 - Terrance and Phillip
                        ##1872: b'Mr. Hankey', \
                        ##1886: b'PC Principal', \
                        ##1923: b'Cupid Cartman', \
                        ##1947: b'Towelie', \
                        # 1948 - Visitors
                        ##1949: b'Bounty Hunter Kyle', \
                        ##1972: b'Dragonslayer Red', \
                        ##1973: b'Classi', \
                        ##1983: b'Imp Tweek', \
                        ##2013: b'Swordsman Garrison', \
                        ##2030: b'President Garrison', \
                        ##2035: b'Mr. Slave Executioner', \
                        # 2041 - Ice Sniper Wendy
                        ##2042: b'Elven King Bradley', \
                        ##2043: b'Priest Maxi', \
                        ##2044: b'Swashbuckler Red', \
                        ##2074: b'Mr Mackey', \
                        ##2080: b'Satan', \
                        ##2081: b'Santa Claus', \
                        ##2091: b'Mosquito', \
                        # 2093 - Mosquito Swarm
                        ##2098: b'Tupperware', \
                        ##2101: b'Alien Drone', \
                        # 2102 - Auto-Vacuum
                        ##2114: b'Sharpshooter Shelly', \
                        ##2117: b'Super Fart', \
                        ##2130: b'The Chomper', \
                        ##2132: b'Fastpass', \
                        ##2136: b'Call Girl', \
                        ##2141: b'The Coon', \
                        ##2143: b'Human Kite', \
                        ##2144: b'Toolshed', \
                        ##2147: b'Mysterion', \
                        # 2169 - Toolshed
                        # 2170 - Professor Chaos
                        # 2171 - Mosquito
                        # 2172 - Tupperware
                        # 2176 - Call Girl
                        # 2177 - Mysterion
                        # 2181 - Fastpass
                        # 2182 - Human Kite
                        # 2183 - Tupperware
                        # 2185 - The Coon
                        ##2190: b'Lava!', \
                        ##2195: b'Doctor Timothy', \
                        ##2200: b'Captain Diabetes', \
                        ##2202: b'Professor Chaos', \
                        ##2209: b'Big Mesquite Murph', \
                        ##2210: b'Sorceress Liane', \
                        ##2216: b'Mintberry Crunch', \
                        ##2217: b'Jesus', \
                        ##2251: b'Sizzler Stuart', \
                        ##2258: b'Mayor McDaniels', \
                        ##2261: b'Wonder Tweek', \
                        ##2262: b'Super Craig', \
                        ##2266: b'Thunderbird', \
                        ##2290: b'General Disarray', \
                        ##2295: b'City Wok Guy', \
                        ##2299: b'Dark Angel Red', \
                        ##2308: b'Space Pilot Bradley', \
                        ##2316: b'Chaos Hamsters', \


                        
##                                        break
                                
                        
                        
                        
                        mitmproxy.ctx.log.info('blocked flow.request.url == ' + repr(flow.request.url))
                        flow.response = mitmproxy.http.HTTPResponse.make(200)
                        break
        def response(self, flow):
##                mitmproxy.ctx.log.info('flow.request.url == ' + repr(flow.request.url))
                if DEF_USE_CUSTOM_UPGRADE_LEVEL[0] and flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/start':
                        o = json.loads(flow.response.content.decode())
##                        mitmproxy.ctx.log.info('len(flow.response.content) == ' + repr(len(flow.response.content)))
                        if 'pvp' in o:
                                del o['pvp']
                        if 'team' in o:
                                del o['team']
                        # causes privacy preferences popup that can't be removed
##                        del o['session']
                        if 'time' in o:
                                del o['time']
                        if 'configuration' in o:
                                del o['configuration']
                        if 'event' in o:
                                del o['event']
                        if 'store' in o:
                                del o['store']
                        if 'control' in o['session']:
                                del o['session']['control']
                        if 'first_login' in o['session']:
                                del o['session']['first_login']
                        if 'country' in o['session']:
                                del o['session']['country']
                        if 'random' in o['session']:
                                del o['session']['random']
                        if 'player_id' in o['session']:
                                del o['session']['player_id']
                        if 'last_login' in o['session']:
                                del o['session']['last_login']
                        # causes popup about account already running at different device
##                        del o['session']['device']
                        if 'setting_bits' in o['session']:
                                del o['session']['setting_bits']
                        if 'gdpr' in o['session']:
                                del o['session']['gdpr']
                        # causes privacy preferences popup that can't be removed
##                        del o['session']['gdpr_consent']
                        o['session']['gdpr_consent'] = int(time.time()) - 180
                        
                        if 'active_gear' in o['player_data']:
                                del o['player_data']['active_gear']
                        if 'stats' in o['player_data']:
                                del o['player_data']['stats']
                        if 'gear' in o['player_data']:
                                del o['player_data']['gear']
                        if 'items' in o['player_data']:
                                del o['player_data']['items']
                        if 'messages' in o['player_data']:
                                del o['player_data']['messages']
                        if 'common' in o['player_data']:
                                del o['player_data']['common']
                        # pvp play button is gone
                        if 'state' in o['player_data']:
                                del o['player_data']['state']
                        if 'avatar' in o['player_data']:
                                del o['player_data']['avatar']
                        # causes game to play opening scene
##                        del o['player_data']['episode']

                        ## level id constants
                        # #1 --- 1327
                        # #2 --- 1344
                        # #3 --- 1338
                        # #4 --- 1326
                        # #5 --- 1312
                        
                        # #6 --- 1400
                        # #7 --- 1475
                        # #8 --- 1401
                        # #9 --- 1476
                        # #10 --- 116
                        
                        # #11 --- 1410
                        # #12 --- 1411
                        # #13 --- 1412
                        # #14 --- 1413
                        # #15 --- 1415
                        
                        # #16 --- 1416
                        # #17 --- 1417
                        # #18 --- 1418
                        # #19 --- 1419
                        # #20 --- 1660
                        
                        # #21 --- 1661
                        # #22 --- 1662
                        # #23 --- 1663
                        # #24 --- 1664
                        # #25 --- 1420
                        
                        # #26 --- 1494
                        # #27 --- 1495
                        # #28 --- 1496
                        # #29 --- 1497
                        # #30 --- 1498
                        
                        # #31 --- 1499
                        # #32 --- 1500
                        # #33 --- 1501
                        # #34 --- 1502
                        # #35 --- 1503
                        
                        # #36 --- 1524
                        # #37 --- 1525
                        # #38 --- 1526
                        # #39 --- 1527
                        # #40 --- 1528
                        
                        # #41 --- 1504
                        # #42 --- 1505
                        # #43 --- 1506
                        # #44 --- 1507
                        # #45 --- 1508
                        
                        # #46 --- 1509
                        # #47 --- 1510
                        # #48 --- 1511
                        # #49 --- 1512
                        # #50 --- 1513
                        
                        # #51 --- 1514
                        # #52 --- 1515
                        # #53 --- 1516
                        # #54 --- 1517
                        # #55 --- 1518
                        
                        # #56 --- 1519
                        # #57 --- 1520
                        # #58 --- 1521
                        # #59 --- 1522
                        # #60 --- 1523
                        
                        o['player_data']['episode'] = [\
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1515, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1514, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1517, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1516, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1518, 'special': 1}\
                                                                   ], 'id': 11, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1509, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1511, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1510, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1513, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1512, 'w': 25, 'l': 25}\
                                                                   ], 'id': 10, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1520, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1519, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1521, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1522, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1523, 'special': 1}\
                                                                   ], 'id': 12, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1326, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1344, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1327, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1312, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1338, 'w': 25, 'l': 25}\
                                                                   ], 'id': 1, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 0, 's': 0, 'id': 2135, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2161, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 1838, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2160, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2156, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2157, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2158, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2159, 'w': 1, 'l': 0}, \
                                                                   {'a': 0, 's': 0, 'id': 2163, 'w': 1, 'l': 0}\
                                                                   ], 'id': 0, 'star_level': 1}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1410, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1411, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1412, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1413, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1415, 'special': 1}\
                                                                   ], 'id': 3, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 116, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1401, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1400, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1476, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1475, 'w': 25, 'l': 25}\
                                                                   ], 'id': 2, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1420, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1664, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1663, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1662, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1661, 'w': 25, 'l': 25}\
                                                                   ], 'id': 5, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1418, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1419, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1660, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1416, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1417, 'w': 25, 'l': 25}\
                                                                   ], 'id': 4, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1502, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1499, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1500, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1501, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1503, 'special': 1}\
                                                                   ], 'id': 7, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1498, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1494, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1495, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1496, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1497, 'w': 25, 'l': 25}\
                                                                   ], 'id': 6, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1508, 'special': 1}, \
                                                                   {'a': 2, 's': 52, 'id': 1506, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1507, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1504, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1505, 'w': 25, 'l': 25}\
                                                                   ], 'id': 9, 'star_level': 4}, \
                                {'node': 0, 'state': 0, 'levels': [{'a': 2, 's': 52, 'id': 1524, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1525, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1526, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 's': 52, 'id': 1527, 'w': 25, 'l': 25}, \
                                                                   {'a': 2, 'l': 25, 's': 52, 'w': 25, 'id': 1528, 'special': 1}\
                                                                   ], 'id': 8, 'star_level': 4}]
                        # connection error
##                        del o['player_data']['balance']
                        o['player_data']['balance'] = [{'code': 'PVP', 'value': 0}, \
                                                       {'code': 'DM', 'value': 0}, \
                                                       {'code': 'CN', 'value': 0}, \
                                                       {'code': 'SUP', 'value': 0}]
                        if 'call_outs' in o['player_data']:
                                del o['player_data']['call_outs']
                        if 'store' in o['player_data']:
                                del o['player_data']['store']
                        if 'decks' in o['player_data']:
                                del o['player_data']['decks']
##                        DEF_CUSTOM_CARDS_temp = 144
##                        DEF_CUSTOM_CARDS[0] = [DEF_CUSTOM_CARDS_temp*10 + 1,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 2,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 3,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 4,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 5,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 6,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 7,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 8,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 9,\
##                                            DEF_CUSTOM_CARDS_temp*10 + 10]
                        o['player_data']['decks'] = {'0': DEF_CUSTOM_CARDS[0]}



                        
                        CharacterIdList = list(CharacterNames)
                        templist = []
                        templist.append({'c': 1, 'id': 1, 'w': 1.1})
                        i = 0
                        upgrade = upgradedict[DEF_UPGRADE_LEVEL[0]]
                        elem_s = upgrade['s']
                        elem_c = upgrade['c']
                        elem_x = upgrade['x']
                        elem_w = upgrade['w']
                        while i < len(CharacterIdList):
                                templist.append({'id': CharacterIdList[i], 's': elem_s, 'c': elem_c, 'x': elem_x, 'w': elem_w})
                                i += 1
                        ## NPC's are being ignored at session start
##                        i = 0
##                        while i < len(DEF_CUSTOM_CARDS[0]):
##                                templist.append({'id': DEF_CUSTOM_CARDS[0][i], 's': elem_s, 'c': elem_c, 'x': elem_x, 'w': elem_w})
##                                i += 1
                        
                        o['player_data']['cards'] = templist
                        
                        flow.response.content = json.dumps(o).encode()
##                        mitmproxy.ctx.log.info('len(flow.response.content) after reencode == ' + repr(len(flow.response.content)))
##                        mitmproxy.ctx.log.info('list(o) == ' + repr(list(o)))
##                        mitmproxy.ctx.log.info("list(o['session']) == " + repr(list(o['session'])))
##                        mitmproxy.ctx.log.info("list(o['player_data']) == " + repr(list(o['player_data'])))
                        mitmproxy.ctx.log.info('o == ' + repr(o))
                        
                

addons = [
        SPPDFilter()
]
