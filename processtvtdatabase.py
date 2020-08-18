import json

enable_team_filter = True
team_filter_team_id_list = [150848]
team_filter_player_id_list = []

profileid_dictionary = {}
file_pointer_position = 0

## Needs to be changed after every week
override_min_time = 1597492800
override_max_time = 1597665600

with open('tvtsheet.csv', 'wb', buffering=0) as db_f_unused:
        pass
        
while True:
        with open('tvtdatabase.db', 'rb', buffering=0) as db_f:
                
                db_f.seek(file_pointer_position)
                read_5 = db_f.read(5)
                if len(read_5) != 5:
                        break
                assert read_5[0:1] == b'\n'
                len_data = int.from_bytes(read_5[1:5], "big")
                data = db_f.read(len_data)
                assert len(data) == len_data
                entry = json.loads(data.decode())
                while True:
                        if entry['flow.response.content.decode()'][0:1] != '{':
                                print('unknown response at file position = ' + str(file_pointer_position))
                                break
                        response = json.loads(entry['flow.response.content.decode()'])
                        try:
                                response_httpCode = response["httpCode"]
                                if response_httpCode == 401 or response_httpCode == 502:
##                                        print('WARNING: Server responded code 401, manual app refresh required!')
                                        break
                        except KeyError:
                                pass
                        team_members_string = "https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/team/members/"
                        team_teams_string = "https://pdc-public-ubiservices.ubi.com/v1/spaces/99e34ec4-be44-4a31-a0a2-64982ae01744/sandboxes/DRAFI_IP_LNCH_PDC_A/team/teams/"
                        if entry["flow.request.url"].startswith(team_members_string):
                                profileid = entry["flow.request.url"][len(team_members_string):]
                                time_time = entry["time.time()"]
                                wins_tw = None

##                                if not 'statistics' in response:
##                                        print ('??? repr(response) == ' + repr(response))
                                if not 'tw' in response['statistics']['wins']:
                                        ## tracker account which does not participate in tvt at all
                                        wins_tw = 0
##                                        print ('??? repr(response) == ' + repr(response))
                                else:
                                        wins_tw = response['statistics']['wins']['tw']
                                if profileid in profileid_dictionary:
                                        (time_time_previous, wins_tw_previous) = profileid_dictionary[profileid]
                                        if wins_tw_previous != wins_tw:
                                                if (enable_team_filter == True and profileid in team_filter_player_id_list) or \
                                                   enable_team_filter == False:
                                                        with open('tvtsheet.csv', 'ab', buffering=0) as db_f_output:
                                                                time_time_previous_copy = time_time_previous
                                                                if time_time_previous_copy < override_min_time:
                                                                        time_time_previous_copy = override_min_time
                                                                if time_time_previous_copy > override_max_time:
                                                                        time_time_previous_copy = override_max_time
                                                                
                                                                time_time_copy = time_time
                                                                if time_time_copy < override_min_time:
                                                                        time_time_copy = override_min_time
                                                                if time_time_copy > override_max_time:
                                                                        time_time_copy = override_max_time
                                                                db_f_output.write(b'"'+profileid.encode()+b'",' + \
                                                                                  b'"'+str(time_time_previous_copy).encode()+b'",' + \
                                                                                  b'"'+str(time_time_copy).encode()+b'",' + \
                                                                                  b'"'+str(wins_tw - wins_tw_previous).encode()+b'"\r\n')
                                                                          
                                profileid_dictionary[profileid] = (time_time, wins_tw)
                        elif entry["flow.request.url"].startswith(team_teams_string) and enable_team_filter:
                                assert len(team_filter_team_id_list) > 0
                                teamid = entry["flow.request.url"][len(team_teams_string):]
                                if int(teamid) in team_filter_team_id_list:
                                        try:
                                                teams_s = response
                                                i = 0
                                                len_teams_s_members = len(teams_s['members'])

                                                i = 0
                                                while i < len_teams_s_members:
                                                        if teams_s['members'][i]['profileId'] not in team_filter_player_id_list:
                                                                team_filter_player_id_list.append(teams_s['members'][i]['profileId'])
                                                        i += 1
                                        except KeyError:
                                                pass
                        
                        break
                file_pointer_position = db_f.tell()

with open('tvtuserlist.py', 'wb', buffering=0) as db_f_userlist:
        if enable_team_filter:
                db_f_userlist.write(repr(team_filter_player_id_list).encode())
        else:
                db_f_userlist.write(repr(list(profileid_dictionary)).encode())
##print ('team_filter_player_id_list == ' + repr(team_filter_player_id_list))
        
