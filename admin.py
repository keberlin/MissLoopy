import optparse
import re
import sys

from sqlalchemy.sql.expression import and_, func, or_

from database import db_init, MISSLOOPY_DB_URI
from iputils import *
import mask
from mlutils import *
from model import *

session = db_init(MISSLOOPY_DB_URI)

parser = optparse.OptionParser()
parser.add_option("-n", "--non-interactive", dest="stdin", action="store_true", help="use stdin for input")

(options, args) = parser.parse_args()


def command(cmd):
    limit = 50
    cmds = cmd.strip().upper().split()
    if len(cmds) == 0:
        return
    if cmds[0] == "LOGIN":
        query = session.query(
            ProfileModel.id,
            ProfileModel.email,
            ProfileModel.name,
            ProfileModel.gender,
            ProfileModel.location,
            ProfileModel.last_ip,
            ProfileModel.last_ip_country,
        ).order_by(ProfileModel.last_login.desc())
    elif cmds[0] == "RECENT":
        query = session.query(
            ProfileModel.id,
            ProfileModel.email,
            ProfileModel.name,
            ProfileModel.gender,
            ProfileModel.location,
            ProfileModel.last_ip,
            ProfileModel.last_ip_country,
        ).order_by(ProfileModel.created2.desc())
    elif cmds[0] == "EMAILS":
        query = (
            session.query(EmailModel.id_from, EmailModel.message)
            .group_by(EmailModel.id_from)
            .group_by(EmailModel.message)
            .order_by(func.max(EmailModel.sent))
        )
        # cmd = "SELECT id_from,message FROM (SELECT DISTINCT id_from,message,MAX(sent) FROM emails GROUP BY id_from,message ORDER BY MAX(sent)) sub LIMIT %d" % (50)
    elif cmds[0].startswith("CONV"):
        id1 = int(cmds[1])
        id2 = int(cmds[2])
        query = (
            session.query(EmailModel.id_from, EmailModel.id_to, EmailModel.message)
            .filter(
                or_(
                    and_(EmailModel.id_from == int(id1), EmailModel.id_to == int(id2)),
                    and_(EmailModel.id_from == int(id2), EmailModel.id_to == int(id1)),
                )
            )
            .order_by(EmailModel.sent)
        )
    try:
        if cmds[0] == "SELECT":
            entries = query.limit(limit).all()
            for entry in entries:
                print(entry)
        session.commit()
    except Exception as e:
        print("Error:", repr(e), "executing:", str(query))


if not sys.stdin.isatty():  # Something available on stdin..
    for line in sys.stdin.readlines():
        command(line)
else:
    while True:
        line = raw_input("SQL: ")
        if line.upper() in ["QUIT", "EXIT"]:
            break
        command(line)
