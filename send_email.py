import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

me = 'YOUR GMAIL SMTP EMAIL ADDRESS'
pwd = 'YOUR GMAIL SMTP PASSWORD'

COMMASPACE = ', '

email_addresses = {
  #'Name of lad in league': "their email", e.g):
  #'Ben Kenobi': "hello-there@high-ground.com",
  #'Zaphod Beeblebrox': "best-bang@since-the-big-one.com"
}

def send_email(lad_who_did_the_worst):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = "GW " + str(lad_who_did_the_worst['gw']) + ": not your week eh " + lad_who_did_the_worst['name'].split()[0] + "?"
    msg['From'] = me
    msg['To'] = email_addresses[lad_who_did_the_worst['name']]
    msg['CC'] = COMMASPACE.join(email_addresses.values())

    html = '''\
    <html>
    <head></head>
    <body>
    <p>'''

    if len(lad_who_did_the_worst['transfers']) > 1:
        html += 'Your transfers; '
        for transfer in lad_who_did_the_worst['transfers']:
            html += transfer['out'] + ' ---> ' + transfer['in'] + ', '
        if lad_who_did_the_worst['hit_cost']:
            html += ' which to remind you cost you ' + str(lad_who_did_the_worst['hit_cost']) + ' points, and thus '
        html += 'netted you a total of ' + str(lad_who_did_the_worst['total_delta']) + ''' points.<br><br>
                <b>Ye good call getting us out you flop!</b><br>'''
        for transfer in lad_who_did_the_worst['transfers']:
            html += '<img src="' + transfer['out_photo'] + '"/>'
    else:
      transfer = lad_who_did_the_worst['transfers'][0]
      html += '''Your transfer ''' + transfer['out'] + ''' to ''' + transfer['in'] + ''' netted you ''' + str(transfer['delta']) + ''' points.<br><br>
         <b>Ye good call getting me out you flop!</b><br>
         <img src="''' + transfer['out_photo'] + '''"/>'''

    html += '''</p>
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
    s.sendmail(me, email_addresses.values(), msg.as_string())
    s.quit()
