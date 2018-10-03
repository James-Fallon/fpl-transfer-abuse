import json, requests
import os
from pprint import pprint
from send_email import send_email

#Variables

league_ID = 271140
gameweek_number = 7

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

def printTransferAndReturnPointsDelta(transfer):
    tr_in = transfer['element_in']
    tr_out = transfer['element_out']

    transfer_string = all_player_details[tr_out]["second_name"] + "\t----->\t" + all_player_details[tr_in]["second_name"]

    tr_out_pnts = all_player_details[tr_out]['event_points']
    tr_in_pnts = all_player_details[tr_in]['event_points']
    delta = tr_in_pnts - tr_out_pnts

    transfer_string += "\t|\tDelta: "
    print(transfer_string, delta)
    return delta

worst_points_delta = "No-one", 0

for id, name in getUsers(league_ID):
    json_transfers = requests.get(transfers_url.format(id)).json()
    print("\n\n" + name)
    print("-----------------------------")
    this_weeks_transfers = [transfer for transfer in json_transfers["history"] if transfer["event"] == gameweek_number]

    worse_single_points_delta = 0
    worst_transfer = {}

    points_delta = 0
    if(len(this_weeks_transfers) > 0):
        for transfer in this_weeks_transfers:
            single_points_delta = printTransferAndReturnPointsDelta(transfer)
            points_delta += single_points_delta
            if single_points_delta < worse_single_points_delta:
                worse_single_points_delta = single_points_delta
                worst_transfer = transfer
        print("Points for transfers: ", points_delta)
    else:
        pprint("No transfers")

    print("-----------------------------")
    if points_delta < worst_points_delta[1]:
        worst_points_delta = name, points_delta

        worst_transfer_of_the_week = {
            'name': name.split()[0],
            'delta': worse_single_points_delta,
            'player_out': all_player_details[worst_transfer['element_out']]["second_name"],
            'player_in':  all_player_details[worst_transfer['element_in']]["second_name"],
            'photo': getPhotoOfPlayer(worst_transfer['element_out'])
        }


send_email(gameweek_number, worst_transfer_of_the_week)
