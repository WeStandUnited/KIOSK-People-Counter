import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime

def daily_update(totalEntered, totalLeft):

    f = open('daily_update.html', 'w')
    contents = """<html>
            <head>
                <meta charset="utf-8" />
                <title>Daily Report</title>
            </head>
            <body style="text-align:center;margin-right: auto;margin-left: auto;>
                <h1 style="text-align:center;margin-right: auto;margin-left: auto;">Welcome to your SUNY Oswego People Counter Kiosk Daily Report!</h1>
                <br />
                <br />
            </div>
            <p></p>
            <p>Total People who entered Shineman this week: %d</p>
            <p></p>
            <p>Total People who left Shineman this week: %d</p>
            <p></p>
            <br />
            <br />
            <p>That's all there is to report. Thank you for your time and enjoy the rest of your evening.</p>
            <p>-Shineman Kiosk</p>
            </body>
            </html>""" % (totalEntered, totalLeft)
    f.write(contents)
    f.close()


def dailyEmail(totalEntered, totalLeft):
    now = datetime.datetime.now()

    if True:
        # create  daily update file
        daily_update(totalEntered, totalLeft)

        # read credentials from file
        filepath = 'credentials.txt'
        with open(filepath) as fp:
            username = fp.readline()
            password = fp.readline()

        # variables for the email
        sender = username

        #enter your email here
        receiver = 'someone@example.com'

        subject = 'People Counter Daily Report'
        body = 'Here is the daily report for the Kiosk Counter in Shineman'

        filepath2 = 'daily_update.html'
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver
        msg.attach(MIMEText(body, 'plain'))
        attachment = open(filepath2, 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filepath2)
        msg.attach(part)
        text = msg.as_string()

        # sending email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.connect("smtp.gmail.com", 587)
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sender, password)
            smtp.sendmail(sender, receiver, text)