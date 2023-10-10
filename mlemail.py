import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# to, subject and message must be in utf-8
# importance = 1 Highest, 2, High, 3 Normal, 4 Low, 5 Lowest
def Email2(sender, to, subject, message, importance=3):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    msg["X-Priority"] = str(importance)
    msg.attach(MIMEText(message, "html"))
    server = smtplib.SMTP("localhost")
    server.sendmail(sender, to, msg.as_string())
    server.quit()
