#!/usr/bin/python

import os

from mlhtml import *

from logger import *

logger.info('%s' % (os.path.basename(__file__)))

Redirect('/seeking')
