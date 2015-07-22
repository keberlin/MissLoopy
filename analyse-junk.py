#!/usr/bin/python

import sys

from utils import *

MANDATORY = ['western union', 'proposal', 'money', 'usd', 'solicitor', 'lawyer', 'barrister', 'lottery', 'lotto', 'sweepstake',
             'transaction', 'bank', 'winner', 'official', 'payout', 'winning', 'orphan', 'cancer', 'moneygram', 'civil war',
             'property', 'transfer', 'refuge', 'million', 'fighting', 'deposit', 'account', 'political', 'assistance', 'relocate',
             'profit', 'worth', 'inherit', 'fortune', 'court', 'death', 'pastor', 'relative', 'tragic', 'fund', 'document',
             'invest', 'honest', 'business', 'urgent', 'willing', 'notification', 'promotion', 'congratulation', 'ticket',
             'results', 'gbp', 'jackpot', 'reference', 'important', 'yahoo', 'gmail', 'hotmail', 'outlook', 'live', 'skype',
             'rocketmail', 'facebook', 'ymail', 'loan', 'dollar', 'apply', 'collateral']

EXCLUSIONS = ['hello']

message_count = 0
keywords = {}

def Process(file,count=1):
  global message_count
  with open(file, 'r') as f:
    messages = set()
    for line in f.readlines():
      if len(line) == 0:
        continue
      junk = line.decode('utf-8','ignore').lower()
      messages.add(re.sub(r'\W+',r' ',junk))
    message_count += len(messages)
    # Put in single words first
    for message in messages:
      ss = message.split()
      if len(ss) < 2:
        continue
      for word in ss:
        if len(word) >= 5:
          if word in keywords:
            keywords[word] += count
          else:
            keywords[word] = count
    # Then double words
    for message in messages:
      ss = message.split()
      if len(ss) < 2:
        continue
      last = ss[0]
      for word in ss[1:]:
        if len(last) >= 2 and len(word) >= 2 and (len(last) >= 4 or len(word) >= 4):
          keyword = last + ' ' + word
          if keyword in keywords:
            keywords[keyword] += count
          else:
            keywords[keyword] = count
        last = word
    # Then triple words
    for message in messages:
      ss = message.split()
      if len(ss) < 2:
        continue
      last1 = ss[0]
      last2 = ss[1]
      for word in ss[2:]:
        if len(last1) >= 2 and len(last2) >= 2 and len(word) >= 2 and (len(last1) >= 4 or len(last2) >= 4 or len(word) >= 4):
          keyword = last1 + ' ' + last2 + ' ' + word
          if keyword in keywords:
            keywords[keyword] += count
          else:
            keywords[keyword] = count
        last1 = last2
        last2 = word

Process(sys.argv[1], 1)
Process(sys.argv[2], 2)

threshold = message_count/75

spam = {}
for item,count in keywords.iteritems():
  if count < threshold:
    continue
  if item in EXCLUSIONS:
    continue
  spam[item.replace(r' ',r'\W+')] = count/float(message_count)
for item in MANDATORY:
  if item in keywords:
    continue
  spam[item.replace(r' ',r'\W+')] = 0.75
with open('spamkeywords.py','w') as f:
  f.write('SPAM_KEYWORDS = '+str(spam)+'\n')
