import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from settings import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PWD, EMAIL_ADDRESSES
from email_constants import *


def create_transfers_table(transfers, hits):
    number_of_free_transfers = len(transfers) - hits
    transfers_table_string = "<table>"
    for x in range(len(transfers)):
        transfer = transfers[x]
        seperator = '<td></td>' if x < number_of_free_transfers else '<td class=\"hit_transfer\">-4</td>'
        transfers_table_string += f"<tr><td class=\"cell\"><img src=\"{transfer['out'].photo_url}\" height=280 width=220></img></td>"
        transfers_table_string += f"<td class=\"cell\"><font size=\"36\">&#8594;</font></td><td class=\"cell\"><img src=\"{transfer['in'].photo_url}\" height=280 width=220></img></td></tr>"
        transfers_table_string += f"<tr><td class=\"cell\">{transfer['out'].name} ({transfer['out'].points} points)</td>{seperator}<td class=\"cell\">{transfer['in'].name} ({transfer['in'].points} points)</td></tr>"
    transfers_table_string += "</table>"
    return transfers_table_string


def send_summary(week_info):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = f"{week_info['league_name']} - GW {week_info['gw_number']} Summary"
    msg['From'] = SMTP_USER
    msg['To'] = COMMASPACE.join(EMAIL_ADDRESSES)

    # MVP
    mvp_details = f"<h3>{week_info['mvp'].name}</h3><p>{week_info['mvp'].team_name}</p><p>&nbsp</p>"
    mvp_transfers_table = create_transfers_table(week_info['mvp'].transfer_details['moves'], week_info['mvp'].number_of_hits_taken)

    # SHITEBAG
    shitebag_details = f"<h3>{week_info['shitebag'].name}</h3><p>{week_info['shitebag'].team_name}</p><p>&nbsp</p>"
    shitebag_transfers_table = create_transfers_table(week_info['shitebag'].transfer_details['moves'], week_info['shitebag'].number_of_hits_taken)

    # MOVEMENTS

    full_html_string = f'''
    <html>
        {HEAD_STRING}
        <body>
            {LEAGUE_AND_GW_HEADING.format(week_info['league_name'], week_info['gw_number'])}
            {VERTICAL_SEPERATOR}
            {MVP_HEADING}
            <center>
                {mvp_details}
                {mvp_transfers_table}
            </center>
            {VERTICAL_SEPERATOR}
            {SHITEBAG_HEADING}
            <center>
                {shitebag_details}
                {shitebag_transfers_table}
            </center>
        </body>
    </html>'''

    html_part = MIMEText(full_html_string, 'html')
    msg.attach(html_part)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    s.ehlo()
    s.login(SMTP_USER, SMTP_PWD)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(SMTP_USER, EMAIL_ADDRESSES, msg.as_string())
    s.quit()
