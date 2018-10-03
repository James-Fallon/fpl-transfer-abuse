import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#me = GMAIL SMTP EMAIL ADDRESS
#pwd = GMAIL SMTP PASSWORD

COMMASPACE = ', '

email_addresses = {
  #'First name of lad in league': "their email",
  #'Ben': "hello-there@high-ground.com",
}

def send_email(gw, transfer):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = "GW " + str(gw) + ": not your week eh " + transfer['name'] + "?"
    msg['From'] = me
    msg['To'] = email_addresses[transfer['name']]
    msg['CC'] = COMMASPACE.join(email_addresses.values())

    html = '''\
    <html>
    <head></head>
    <body>
    <p>Your transfer ''' + transfer['player_out'] + ''' to ''' + transfer['player_in'] + ''' netted you ''' + str(transfer['delta']) + ''' points.<br><br>
       <b>Ye good call getting me out you flop!</b><br>
       <img src="''' + transfer['photo'] + '''"/>
    </p>
    </body>
    </html>
    '''

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(me, pwd)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, email_addresses[transfer['name']], msg.as_string())
    s.quit()
