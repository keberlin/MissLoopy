#!/usr/bin/python

import fileinput, spam

MAX_LENGTH = 100

for line in fileinput.input():
  if len(line) == 0:
    continue
  message = line.decode('utf-8','ignore').lower()
  tuple = spam.AnalyseSpam(message)
  print 'score:%d density:%d hits:%s "%s..."' % (tuple[0], tuple[1], tuple[2], message.encode('utf-8')[:MAX_LENGTH])
