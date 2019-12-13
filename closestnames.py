import os

from utils import *
from gazetteer import *
from mljson import *

from logger import *

MAX_MATCHES = 5

dict = FetchFormFields()

logger.info('%s: %s' % (os.path.basename(__file__), repr(dict)))

if not 'query' in dict:
  Error('No query specified.')

query = dict['query'].lstrip()

closest = GazClosestMatchesQuick(query, MAX_MATCHES)

Return({'matches':closest})
