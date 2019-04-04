import json, requests
import os
from pprint import pprint
from send_email import send_email
from send_email_summary import send_summary

# Change these to true to send emails
should_send_summary = False
should_send_who_messed_up = False

#Variables
league_ID = 271140

# FPL API Endpoints
transfers_url = 'https://fantasy.premierleague.com/drf/entry/{}/transfers'
league_details_url = 'http://fantasy.premierleague.com/drf/leagues-classic-standings/{}?phase=1&le-page=1&ls-page=1'

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

def getChipPlayed(userId, gw_num):
    return requests.get("https://fantasy.premierleague.com/drf/entry/" + str(userId) + "/event/" + str(gw_num) + "/picks").json()["active_chip"]

def getLeagueName(league_id):
    return requests.get(league_details_url.format(str(league_id))).json()["league"]["name"]

def getUsers(league_id):
    jsonResponse = requests.get(league_details_url.format(str(league_id))).json()
    standings = jsonResponse["standings"]["results"]
    return list(map(lambda x: (x["entry"], x["player_name"], x["entry_name"]), standings))

def parseTransfer(transfer):
    tr_in = transfer['element_in']
    tr_out = transfer['element_out']

    tr_out_pnts = all_player_details[tr_out]['event_points']
    tr_in_pnts = all_player_details[tr_in]['event_points']
    delta = tr_in_pnts - tr_out_pnts

    parsedTransfer = {
        'out': all_player_details[tr_out]['web_name'],
        'out_points': tr_out_pnts,
        'out_photo': getPhotoOfPlayer(tr_out),
        'in': all_player_details[tr_in]['web_name'],
        'in_points': tr_in_pnts,
        'in_photo': getPhotoOfPlayer(tr_in),
        'delta': delta,
    }
    return parsedTransfer

lads_and_their_transfers = {}

for id, name, team_name in getUsers(league_ID):
    json_transfers = requests.get(transfers_url.format(id)).json()
    current_gameweek_number = json_transfers['entry']['current_event']

    didHeHaveAFreeTransfer = False
    for gw_number in range(2,current_gameweek_number):
        count = 0
        for transfer in json_transfers['history']:
            if transfer['event'] == gw_number:
                count = count + 1
        didHeHaveAFreeTransfer = (count == 0) or (didHeHaveAFreeTransfer and count < 2)

    this_weeks_transfers = [parseTransfer(transfer) for transfer in json_transfers["history"] if transfer["event"] == current_gameweek_number]

    total_delta = 0
    for transfer in this_weeks_transfers:
        total_delta += transfer['delta']

    chip_played = getChipPlayed(id, current_gameweek_number)

    #See if a hit was taken
    hit_cost = 0
    extra_transfers = 0
    if chip_played != 'freehit' and chip_played != 'wildcard':
        num_allowed_transfers = (2 if didHeHaveAFreeTransfer else 1)

        extra_transfers = len(this_weeks_transfers) - num_allowed_transfers
        if extra_transfers > 0:
            hit_cost = extra_transfers * -4

    total_delta += hit_cost

    this_lads_details = {
        'name': name,
        'team_name': team_name,
        'transfers': this_weeks_transfers,
        'total_delta': total_delta,
        'chip_played': chip_played,
        'gw': current_gameweek_number,
        'hits': extra_transfers,
        'hit_cost': hit_cost
    }

    lads_and_their_transfers[id] = this_lads_details

best_delta = -1, 0
worst_delta = -1, 0
for lad in lads_and_their_transfers:
    this_lads_total_delta = lads_and_their_transfers[lad]['total_delta']
    this_lads_played_chip = lads_and_their_transfers[lad]['chip_played']

    if this_lads_total_delta < worst_delta[1] and this_lads_played_chip != 'wildcard' and this_lads_played_chip != 'freehit':
        worst_delta = lad, this_lads_total_delta
    if this_lads_total_delta > best_delta[1] and this_lads_played_chip != 'wildcard' and this_lads_played_chip != 'freehit':
        best_delta = lad, this_lads_total_delta

if worst_delta[0] == -1:
    print("No-one messed up this week. No email will be sent.")
else:
    print('\nWorst Call:\n')
    pprint(lads_and_their_transfers[worst_delta[0]])
    if should_send_who_messed_up:
        send_email(lads_and_their_transfers[worst_delta[0]])

if (worst_delta[0] != -1) and (best_delta[0] != -1) and should_send_summary:
    week_info = {
        'league_name': getLeagueName(league_ID),
        'gw_number': current_gameweek_number,
        'mvp': lads_and_their_transfers[best_delta[0]],
        'shitebag': lads_and_their_transfers[worst_delta[0]]
    }
    pprint(week_info);
    send_summary(week_info)
