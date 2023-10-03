import os
import socket
import time

import dbserverinfo


def sendmsg(message):
  # Connect to the server
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((dbserverinfo.HOST, dbserverinfo.PORT))

  # Send the data
  message = '%d %s' % (os.getpid(), message)
  print 'Sending : "%s"' % message
  s.sendall(message)

  # Receive a response
  response = s.recv(1024)

  # Clean up
  s.close()

sendmsg('acquire read')
print '%d Locked...' % (os.getpid())
time.sleep(2)
print '%d Unlocked...' % (os.getpid())
sendmsg('release read')
