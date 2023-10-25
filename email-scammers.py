import fileinput

from emails import *
from logger import logger
from utils import *

emails = set()
for line in fileinput.input():
    email = line
    emails.add(email)

for email in emails:
    EmailVerify(session, email, 1)
