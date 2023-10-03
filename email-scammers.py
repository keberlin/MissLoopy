import fileinput

from emails import *
from utils import *

emails = set()
for line in fileinput.input():
  email = line.decode('utf-8', 'ignore')
  emails.add(email)

for email in emails:
  EmailVerify(email, 1)
