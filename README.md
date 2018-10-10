# fpl-transfer-abuse
Finds who made the worst transfers in your mini-league this week and sends the poor lad an e-mail letting him know.

## Install
Written for Python 3.6.5.
Run `pip install -r requirements.txt` to install dependencies.

## Run
You'll need to replace the league ID in `transfer_nightmares.py` with your own league ID. Then just run `python transfer_nightmares.py`

## Send email
In `send_email.py` you'll have to enter the first names and email addresses of your league members in the `email-addresses` dict, and enter a valid Gmail SMTP email/pwd combo at the the top of the file.
