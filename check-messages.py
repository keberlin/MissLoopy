import re
import sys

from database import db_init
from mlutils import *
from model import *
import spam

session = db_init()

MAX_LENGTH = 100

for arg in sys.argv[1:]:
    id = int(arg)
    density_min = 9999
    spammer = spam.AnalyseSpammer(id)
    entries = (
        session.query(EmailModel.message).filter(EmailModel.id_from == id).order_by(EmailModel.sent).distinct().all()
    )
    for entry in entries:
        message = re.sub("[\r\n]+", " ", entry.message)
        tuple = spam.AnalyseSpam(message)
        if spam.IsSpamFactored(tuple, spammer, 2):
            print(
                'Potential Spam id:%d "%s..." {score:%d, density:%d, hits:%s}'
                % (id, message[:MAX_LENGTH], tuple[0], tuple[1], tuple[2])
            )
        if tuple[1]:
            density_min = min(density_min, tuple[1])
    print("id:%d members:%d frequency:%.1f min density:%d" % (id, spammer[0], spammer[1] / float(60 * 60), density_min))
