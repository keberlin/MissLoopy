import smtplib, database, mask

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from html import *

FROM = TITLE + '<noreply@' + DOMAIN + '>'

# to, subject and message must be in utf-8
# importance = 1 Highest, 2, High, 3 Normal, 4 Low, 5 Lowest
def Email(to,subject,message,importance=3):
  msg = MIMEMultipart('alternative')
  msg['Subject']    = subject
  msg['From']       = FROM
  msg['To']         = to
  msg['X-Priority'] = str(importance)
  msg.attach(MIMEText(message, 'html'))
  try:
    server = smtplib.SMTP('localhost')
    server.sendmail(FROM, [to], msg.as_string())
    server.quit()
  except:
    pass
