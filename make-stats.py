import argparse
import collections
import sys

from sqlalchemy import create_engine

import mask
from database import MISSLOOPY_DB_URI, db_init
from gazetteer import *
from localization import *
from mlhtml import *
from mlutils import *
from model import *
from tzone import *
from units import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)

YEARS = [1,2,5]

ReportStruct = collections.namedtuple('ReportStruct', 'logged verified unverified males females men women sugar_pups sugar_babies sugar_daddies sugar_mommas avg_age_males avg_age_females avg_age_men avg_age_women avg_age_sugar_pups avg_age_sugar_babies avg_age_sugar_daddies avg_age_sugar_mommas white black latino indian asian mixed other active messages')

parser = argparse.ArgumentParser(description='Generate Static Pages.')
parser.add_argument('-s', metavar='title', nargs=1, help='title of page')
args = parser.parse_args()

BASE_DIR = os.path.dirname(__file__)

now = datetime.datetime.utcnow()

years = {}
for year in YEARS:
  td = now-datetime.timedelta(weeks=year*52)
  entries = session.query(ReportModel).filter(ReportModel.logged>td).order_by(ReportModel.logged).all()
  years[year] = [ReportStruct(report.logged.strftime('%Y-%m-%d'),report.verified,report.unverified,report.males,report.females,report.men,report.women,report.sugar_pups,report.sugar_babies,report.sugar_daddies,report.sugar_mommas,report.avg_age_males,report.avg_age_females,report.avg_age_men,report.avg_age_women,report.avg_age_sugar_pups,report.avg_age_sugar_babies,report.avg_age_sugar_daddies,report.avg_age_sugar_mommas,report.white,report.black,report.latino,report.indian,report.asian,report.mixed,report.other,report.active,report.messages) for report in entries]

d = {'title':'Statistics', 'years':years}

print RenderY('stats.html', d)
