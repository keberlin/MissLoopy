from gazetteer import *
from mljson import *
from utils import *

MAX_MATCHES = 5

dict = FetchFormFields()

if not 'query' in dict:
  Error('No query specified.')

query = dict['query'].lstrip()

closest = GazClosestMatchesQuick(query, MAX_MATCHES)

Return({'matches':closest})
