import fileinput

from emails import *
from utils import *

logging.basicConfig(filename="/var/log/missloopy/log", logging.INFO)

emails = set()
for line in fileinput.input():
    email = line
    emails.add(email)

for email in emails:
    EmailVerify(email, 1)
