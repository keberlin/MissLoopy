#!/usr/bin/python

import cgi

from mlhtml import *

form = cgi.FieldStorage()
data = dict([(x,form.getvalue(x)) for x in form.keys()])
params = '&'.join(map(lambda x:'%s=%s'%(x,data[x]), data.keys()))

Redirect('/test?%s' % params)
