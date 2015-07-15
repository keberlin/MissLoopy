#!/usr/bin/python

import os, cgi

from mlhtml import *

from logger import *

logger.info('%s' % (os.path.basename(__file__)))

form = cgi.FieldStorage()
data = dict([(x,form.getvalue(x)) for x in form.keys()])
params = '&'.join(map(lambda x:'%s=%s'%(x,data[x]), data.keys()))

Redirect('/emailthread?%s' % params)
