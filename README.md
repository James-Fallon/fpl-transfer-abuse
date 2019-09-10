# fpl-transfer-abuse
Finds who made the best and worst transfers in your mini-league this week and sends a group email letting everyone know.

![Sample Email](https://raw.github.com/James-Fallon/fpl-transfer-abuse/master/img/summary.png)

## Install
Written for Python 3.6.5.
Run `pip install -r requirements.txt` to install dependencies.

## Configure
In settings.py, you'll have to add the following:
 - Your FPL login details (This year the FPL API needs authentication)
 - Details of an SMTP email (Used for sending the email summary)
 - List of email addresses to send it to

## Run
` python transfer_nightmares.py --league-id=<your_league_id>` 

with your own league ID.
