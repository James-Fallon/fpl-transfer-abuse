import json, requests
import os
from pprint import pprint
from send_email import send_email

#Variables
league_ID = 271140

# FPL API Endpoints
transfers_url = 'https://fantasy.premierleague.com/drf/entry/{}/transfers'
all_player_details_json = (requests.get('https://fantasy.premierleague.com/drf/bootstrap-static').json())["elements"]

# Parse player-details into id-indexed dict
all_player_details = {}
for i in range(len(all_player_details_json)):
    id = all_player_details_json[i]["id"]
    all_player_details[id] = all_player_details_json[i]

def getPhotoOfPlayer(playerId):
    photo_id = all_player_details[playerId]["photo"]
    pre, ext = os.path.splitext(photo_id)
    photo_png_file = pre + ".png"
    photo_url = "https://platform-static-files.s3.amazonaws.com/premierleague/photos/players/110x140/p" + photo_png_file
    return photo_url

def getUsers(league_id):
    league_url = "http://fantasy.premierleague.com/drf/leagues-classic-standings/" + str(league_id) + "?phase=1&le-page=1&ls-page=1"
    jsonResponse = requests.get(league_url).json()
    standings = jsonResponse["standings"]["results"]
    return list(map(lambda x: (x["entry"], x["player_name"]), standings))

def parseTransfer(transfer):
    tr_in = transfer['element_in']
    tr_out = transfer['element_out']

    tr_out_pnts = all_player_details[tr_out]['event_points']
    tr_in_pnts = all_player_details[tr_in]['event_points']
    delta = tr_in_pnts - tr_out_pnts

    parsedTransfer = {
        'out': all_player_details[tr_out]['web_name'],
        'in': all_player_details[tr_in]['web_name'],
        'delta': delta,
        'out_photo': getPhotoOfPlayer(tr_out)
    }
    return parsedTransfer

lads_and_their_transfers = {}

for id, name in getUsers(league_ID):
    json_transfers = requests.get(transfers_url.format(id)).json()
    current_gameweek_number = json_transfers['entry']['current_event']

    this_weeks_transfers = [parseTransfer(transfer) for transfer in json_transfers["history"] if transfer["event"] == current_gameweek_number]

    total_delta = 0
    for transfer in this_weeks_transfers:
        total_delta += transfer['delta']

    has_wildcarded = False

    for wildcard in json_transfers['wildcards']:
        if wildcard['event'] == current_gameweek_number:
            has_wildcarded = True

    this_lads_details = {
        'name': name,
        'transfers': this_weeks_transfers,
        'total_delta': total_delta,
        'on_wildcard': has_wildcarded,
        'gw': current_gameweek_number
    }

    lads_and_their_transfers[id] = this_lads_details

worst_delta = -1, 0
for lad in lads_and_their_transfers:
    lads_total_delta = lads_and_their_transfers[lad]['total_delta']
    if lads_total_delta < worst_delta[1]:
        worst_delta = lad, lads_total_delta

if worst_delta[0] == -1:
    print("No-one messed up this week")
else:
    pprint(lads_and_their_transfers[worst_delta[0]])
    #send_email(lads_and_their_transfers[worst_delta[0]])
