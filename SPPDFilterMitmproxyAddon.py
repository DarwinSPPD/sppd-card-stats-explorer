## This python script requires mitmproxy library. Install it with following command: Scripts\pip.exe install mitmproxy
##
## Usage command: Scripts\mitmweb.exe -s ./SPPDFilterMitmproxyAddon.py
##
## Somewhat complete mitmproxy API documentation is available by using this command: python.exe -m pydoc mitmproxy
## (third party tutorials about mitmproxy were more helpful than supplied documentation, sorry developers about this)
##
## On target device change proxy to point at mitmproxy's endpoint (port 8080,
## IP address == local IP adress for machine, usually comes in form 192.168.xxx.xxx),
## visit internal website mitm.it and follow instructions to install certificate for SSL connection interception
##
#######
##
## Upon successful setup, this plugin should be able to rewrite card levels and upgrades, 
## allow user to open SPPD deckbuilder and explore card stats for chosen upgrade and
## block every other SPPD functionality.
## No attempts should be made to work around restrictions and use any other features while this plugin is running.


import mitmproxy
import json

## Change DEF_UPGRADE_LEVEL variable listed below to change levels and upgrades shown in SPPD deckbuilder
## Restart of SPPD app is required after every change.

DEF_UPGRADE_LEVEL = ['lvl 1, 1/5']

## Possible values below

##'lvl 1, 1/5'
##'lvl 1, 2/5'
##'lvl 1, 3/5'
##'lvl 1, 4/5'
##'lvl 1, 5/5'
##'lvl 2, 5/15'
##'lvl 2, 6/15'
##'lvl 2, 7/15'
##'lvl 2, 8/15'
##'lvl 2, 9/15'
##'lvl 2, 10/15'
##'lvl 2, 11/15'
##'lvl 2, 12/15'
##'lvl 2, 13/15'
##'lvl 2, 14/15'
##'lvl 2, 15/15'
##'lvl 3, 15/25'
##'lvl 3, 16/25'
##'lvl 3, 17/25'
##'lvl 3, 18/25'
##'lvl 3, 19/25'
##'lvl 3, 20/25'
##'lvl 3, 21/25'
##'lvl 3, 22/25'
##'lvl 3, 23/25'
##'lvl 3, 24/25'
##'lvl 3, 25/25'
##'lvl 4, 25/40'
##'lvl 4, 26/40'
##'lvl 4, 27/40'
##'lvl 4, 28/40'
##'lvl 4, 29/40'
##'lvl 4, 30/40'
##'lvl 4, 31/40'
##'lvl 4, 32/40'
##'lvl 4, 33/40'
##'lvl 4, 34/40'
##'lvl 4, 35/40'
##'lvl 4, 36/40'
##'lvl 4, 37/40'
##'lvl 4, 38/40'
##'lvl 4, 39/40'
##'lvl 4, 40/40'
##'lvl 5, 40/55'
##'lvl 5, 41/55'
##'lvl 5, 42/55'
##'lvl 5, 43/55'
##'lvl 5, 44/55'
##'lvl 5, 45/55'
##'lvl 5, 46/55'
##'lvl 5, 47/55'
##'lvl 5, 48/55'
##'lvl 5, 49/55'
##'lvl 5, 50/55'
##'lvl 5, 51/55'
##'lvl 5, 52/55'
##'lvl 5, 53/55'
##'lvl 5, 54/55'
##'lvl 5, 55/55'
##'lvl 6, 55/70'
##'lvl 6, 56/70'
##'lvl 6, 57/70'
##'lvl 6, 58/70'
##'lvl 6, 59/70'
##'lvl 6, 60/70'
##'lvl 6, 61/70'
##'lvl 6, 62/70'
##'lvl 6, 63/70'
##'lvl 6, 64/70'
##'lvl 6, 65/70'
##'lvl 6, 66/70'
##'lvl 6, 67/70'
##'lvl 6, 68/70'
##'lvl 6, 69/70'
##'lvl 6, 70/70'
##'lvl 7, 70/70'

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
                        if flow.request.url.startswith('https://app-measurement.com/'):
                                break
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
                        if flow.request.url == 'https://www.googleapis.com/games/v1/events?language=en-US':
                                break
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
                        if flow.request.url == 'https://ssl.google-analytics.com/batch':
                                break
                        if flow.request.url == 'https://msr-public-ubiservices.ubi.com/v1/spaces/news?spaceId=1a49a190-9703-4460-91fc-f17c4314ecc3':
                                break
                        if flow.request.url.startswith('https://gamecfg-mob.ubi.com/profile/?action=register&productid=682'):
                                break
                        if flow.request.url.startswith('https://ubistatic-a.akamaihd.net/0081/'):
                                break
##                        if flow.request.url == 'https://msr-public-ubiservices.ubi.com/v2/profiles/ece1f966-ec43-44f5-89dd-9d2e98fba81e/events':
##                                break
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
                        if flow.request.url == 'https://android.clients.google.com/fdfe/skuDetails':
                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/profiles/ubimobile':
                                break
##                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/gamestate/entries':
##                                break
##                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/achievement/status':
##                                break
                        if flow.request.url == 'https://android.clients.google.com/fdfe/ees/bulkAcquire?nocache_qos=lt':
                                break
                        if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/start':
                                break
                        
                        mitmproxy.ctx.log.info('blocked flow.request.url == ' + repr(flow.request.url))
                        flow.response = mitmproxy.http.HTTPResponse.make(200)
                        break
        def response(self, flow):
##                mitmproxy.ctx.log.info('flow.request.url == ' + repr(flow.request.url))
                if flow.request.url == 'https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/session/start':
                        o = json.loads(flow.response.content.decode())
##                        mitmproxy.ctx.log.info('len(flow.response.content) == ' + repr(len(flow.response.content)))
                        del o['pvp']
                        del o['team']
                        # causes privacy preferences popup that can't be removed
##                        del o['session']
                        del o['time']
                        del o['configuration']
                        del o['event']
                        del o['store']
                        del o['session']['control']
                        del o['session']['first_login']
                        del o['session']['country']
                        del o['session']['random']
                        del o['session']['player_id']
                        del o['session']['last_login']
                        # causes popup about account already running at different device
##                        del o['session']['device']
                        del o['session']['setting_bits']
                        del o['session']['gdpr']
                        # causes privacy preferences popup that can't be removed
##                        del o['session']['gdpr_consent']
                        del o['player_data']['active_gear']
                        del o['player_data']['stats']
                        del o['player_data']['gear']
                        del o['player_data']['items']
                        del o['player_data']['messages']
                        del o['player_data']['common']
                        # pvp play button is gone
                        del o['player_data']['state']
                        del o['player_data']['avatar']
                        # causes game to play opening scene
##                        del o['player_data']['episode']
                        # connection error
##                        del o['player_data']['balance']
                        o['player_data']['balance'] = [{'code': 'PVP', 'value': 0}, {'code': 'DM', 'value': 0}, {'code': 'CN', 'value': 0}, {'code': 'SUP', 'value': 0}]
                        del o['player_data']['call_outs']
                        del o['player_data']['store']
                        del o['player_data']['decks']



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
                        CharacterIdList = list(CharacterNames)
                        templist = []
                        templist.append({'c': 1, 'id': 1, 'w': 1.1})
                        i = 0
                        while i < len(CharacterIdList):
                                upgrade = upgradedict[DEF_UPGRADE_LEVEL[0]]
                                elem_s = upgrade['s']
                                elem_c = upgrade['c']
                                elem_x = upgrade['x']
                                elem_w = upgrade['w']
                                templist.append({'id': CharacterIdList[i], 's': elem_s, 'c': elem_c, 'x': elem_x, 'w': elem_w})
                                i += 1

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
