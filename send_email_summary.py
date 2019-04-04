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

def create_transfers_table(transfers, hits):
    number_of_free_transfers = len(transfers) - hits
    transfers_table_string = "<table>"
    for x in range(len(transfers)):
        transfer = transfers[x]
        seperator = '<td></td>' if x < number_of_free_transfers else '<td class=\"hit_transfer\">-4</td>'
        transfers_table_string += f"<tr><td class=\"cell\"><img src=\"{transfer['out_photo']}\" height=280 width=220></img></td>"
        transfers_table_string += f"<td class=\"cell\"><font size=\"36\">&#8594;</font></td><td class=\"cell\"><img src=\"{transfer['in_photo']}\" height=280 width=220></img></td></tr>"
        transfers_table_string += f"<tr><td class=\"cell\">{transfer['out']} ({transfer['out_points']} points)</td>{seperator}<td class=\"cell\">{transfer['in']} ({transfer['in_points']} points)</td></tr>"
    transfers_table_string += "</table>"
    return transfers_table_string

def send_summary(week_info):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = f"{week_info['league_name']} - GW {week_info['gw_number']} Summary"
    msg['From'] = me
    msg['To'] = COMMASPACE.join(email_addresses.values())

    head_string = '''\
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <style type="text/css" media="screen">
        table{
            background-color: #90CCF4;
            empty-cells:hide;
        }
        td.cell{
            background-color: white;
            text-align: center;
        }
        td.hit_transfer{
            background-color: #F78888;
            text-align: center;
            color: white;
        }
    	h2 {
    	  color: #90CCF4;
    	  border-bottom: 1px solid #000000;
    	  border-right: 1px solid #000000;
    	  display: table;
    	}
    	h3 {
    		padding: 0px;
    		margin: 0px;
    	}
    	p {
    		padding: 5px;
    		margin: 0px;
    	}
      </style>
    </head>'''

    vertical_seperator = "<hr>"
    main_heading = f"<center><h1>{week_info['league_name']}<br>GW {week_info['gw_number']}</h1></center>"

    # MVP
    mvp_heading = "<h2>&#9734; MVP &nbsp</h2>"
    mvp_details = f"<h3>{week_info['mvp']['name']}</h3><p>{week_info['mvp']['team_name']}</p><p>&nbsp</p>"
    mvp_transfers_table = create_transfers_table(week_info['mvp']['transfers'], week_info['mvp']['hits'])

    # SHITEBAG
    shitebag_heading = "<h2>&#9760; Shitebag &nbsp</h2>"
    shitebag_details = f"<h3>{week_info['shitebag']['name']}</h3><p>{week_info['shitebag']['team_name']}</p><p>&nbsp</p>"
    shitebag_transfers_table = create_transfers_table(week_info['shitebag']['transfers'], week_info['shitebag']['hits'])

    # MOVEMENTS


    full_html_string = f'''
    <html>
        {head_string}
        <body>
            {main_heading}
            {vertical_seperator}
            {mvp_heading}
            <center>
                {mvp_details}
                {mvp_transfers_table}
            </center>
            {vertical_seperator}
            {shitebag_heading}
            <center>
                {shitebag_details}
                {shitebag_transfers_table}
            </center>
        </body>
    </html>'''

    html_part = MIMEText(full_html_string, 'html')
    msg.attach(html_part)

    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.ehlo()
    s.login(me, pwd)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, email_addresses.values(), msg.as_string())
    s.quit()
