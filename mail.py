import smtplib

from os.path import basename

from email.mime.application import MIMEApplication

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, send_cc, subject, text, file=None,

              server="10.97.95.27"):

    msg = MIMEMultipart()

    msg['From'] = send_from

    msg['To'] = send_to

    msg['CC'] = send_cc

    msg['Date'] = formatdate(localtime=True)

    msg['Subject'] = subject


    msg.attach(MIMEText(text))


    smtp = smtplib.SMTP(server)

    smtp.send_message(msg)

    smtp.close()
