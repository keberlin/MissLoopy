from datetime import datetime, timedelta

from database import db_init, MISSLOOPY_DB_URI
from logger import logger
from mlutils import *
from model import *
from utils import *

session = db_init(MISSLOOPY_DB_URI)


def Bit(enum):
    b = 0
    while not enum & (1 << b):
        b += 1
    return b


now = datetime.utcnow()

verified = 0
unverified = 0
genders = [0, 0, 0, 0, 0, 0]
ages = [0, 0, 0, 0, 0, 0]
ethnicities = [0, 0, 0, 0, 0, 0, 0]

entries = session.query(ProfileModel).all()
for entry in entries:
    if not entry.verified:
        unverified += 1
        continue
    verified += 1
    genders[Bit(entry.gender)] += 1
    ages[Bit(entry.gender)] += Age(entry.dob)
    ethnicities[Bit(entry.ethnicity)] += 1

men = genders[Bit(GEN_MAN)]
women = genders[Bit(GEN_WOMAN)]
sugar_pups = genders[Bit(GEN_SUGAR_PUP)]
sugar_babies = genders[Bit(GEN_SUGAR_BABY)]
sugar_daddies = genders[Bit(GEN_SUGAR_DADDY)]
sugar_mommas = genders[Bit(GEN_SUGAR_MOMMA)]

males = men + sugar_pups + sugar_daddies
females = women + sugar_babies + sugar_mommas
ages_males = ages[Bit(GEN_MAN)] + ages[Bit(GEN_SUGAR_PUP)] + ages[Bit(GEN_SUGAR_DADDY)]
ages_females = ages[Bit(GEN_WOMAN)] + ages[Bit(GEN_SUGAR_BABY)] + ages[Bit(GEN_SUGAR_MOMMA)]

avg_age_males = (ages_males / float(males)) if males else 0
avg_age_females = (ages_females / float(females)) if females else 0
avg_age_men = (ages[Bit(GEN_MAN)] / float(men)) if men else 0
avg_age_women = (ages[Bit(GEN_WOMAN)] / float(women)) if women else 0
avg_age_sugar_pups = (ages[Bit(GEN_SUGAR_PUP)] / float(sugar_pups)) if sugar_pups else 0
avg_age_sugar_babies = (ages[Bit(GEN_SUGAR_BABY)] / float(sugar_babies)) if sugar_babies else 0
avg_age_sugar_daddies = (ages[Bit(GEN_SUGAR_DADDY)] / float(sugar_daddies)) if sugar_daddies else 0
avg_age_sugar_mommas = (ages[Bit(GEN_SUGAR_MOMMA)] / float(sugar_mommas)) if sugar_mommas else 0

white = ethnicities[Bit(ETH_WHITE)]
black = ethnicities[Bit(ETH_BLACK)]
latino = ethnicities[Bit(ETH_LATINO)]
indian = ethnicities[Bit(ETH_INDIAN)]
asian = ethnicities[Bit(ETH_ASIAN)]
mixed = ethnicities[Bit(ETH_MIXED)]
other = ethnicities[Bit(ETH_OTHER)]

# Get number of active profiles (logged in within the last month)
active = (
    session.query(func.count())
    .select_from(ProfileModel)
    .filter(ProfileModel.verified.is_(True))
    .filter(ProfileModel.last_login >= now - timedelta(days=30))
    .scalar()
)

# Get number of sent messages (within the last month)
messages = (
    session.query(func.count()).select_from(EmailModel).filter(EmailModel.sent >= now - timedelta(days=30)).scalar()
)

# Get most blocked members
entries = (
    session.query(BlockedModel.id_block, func.count(BlockedModel.id.distinct()))
    .group_by(BlockedModel.id_block)
    .order_by(func.count(BlockedModel.id.distinct()).desc())
    .limit(10)
    .all()
)
most_blocked = [(entry.id_block) for entry in entries]

# Get most favorite members
entries = (
    session.query(FavoriteModel.id_favorite, func.count(FavoriteModel.id.distinct()))
    .group_by(FavoriteModel.id_favorite)
    .order_by(func.count(FavoriteModel.id.distinct()).desc())
    .limit(10)
    .all()
)
most_favorite = [(entry.id_favorite) for entry in entries]

stats = ReportModel(
    logged=now,
    verified=verified,
    unverified=unverified,
    males=males,
    females=females,
    men=men,
    women=women,
    sugar_pups=sugar_pups,
    sugar_babies=sugar_babies,
    sugar_daddies=sugar_daddies,
    sugar_mommas=sugar_mommas,
    avg_age_males=avg_age_males,
    avg_age_females=avg_age_females,
    avg_age_men=avg_age_men,
    avg_age_women=avg_age_women,
    avg_age_sugar_pups=avg_age_sugar_pups,
    avg_age_sugar_babies=avg_age_sugar_babies,
    avg_age_sugar_daddies=avg_age_sugar_daddies,
    avg_age_sugar_mommas=avg_age_sugar_mommas,
    white=white,
    black=black,
    latino=latino,
    indian=indian,
    asian=asian,
    mixed=mixed,
    other=other,
    active=active,
    messages=messages,
)
session.add(stats)
session.commit()

if __name__ == "__main__":
    print("Number of verified profiles    : %6d" % (verified))
    print("Number of unverified profiles  : %6d" % (unverified))
    print("Number of males                : %6d %4.1f%%" % (males, males * 100 / float(verified)))
    print("Number of females              : %6d %4.1f%%" % (females, females * 100 / float(verified)))
    print("Number of Men                  : %6d %4.1f%%" % (men, men * 100 / float(verified)))
    print("Number of Women                : %6d %4.1f%%" % (women, women * 100 / float(verified)))
    print("Number of Sugar Pups           : %6d %4.1f%%" % (sugar_pups, sugar_pups * 100 / float(verified)))
    print("Number of Sugar Babies         : %6d %4.1f%%" % (sugar_babies, sugar_babies * 100 / float(verified)))
    print("Number of Sugar Daddies        : %6d %4.1f%%" % (sugar_daddies, sugar_daddies * 100 / float(verified)))
    print("Number of Sugar Mommas         : %6d %4.1f%%" % (sugar_mommas, sugar_mommas * 100 / float(verified)))
    print("Average age of males           : %6.1f" % (avg_age_males))
    print("Average age of females         : %6.1f" % (avg_age_females))
    print("Average age of Men             : %6.1f" % (avg_age_men))
    print("Average age of Women           : %6.1f" % (avg_age_women))
    print("Average age of Sugar Pups      : %6.1f" % (avg_age_sugar_pups))
    print("Average age of Sugar Babies    : %6.1f" % (avg_age_sugar_babies))
    print("Average age of Sugar Daddies   : %6.1f" % (avg_age_sugar_daddies))
    print("Average age of Sugar Mommas    : %6.1f" % (avg_age_sugar_mommas))
    print("Number of White                : %6d %4.1f%%" % (white, white * 100 / float(verified)))
    print("Number of Black                : %6d %4.1f%%" % (black, black * 100 / float(verified)))
    print("Number of Latino               : %6d %4.1f%%" % (latino, latino * 100 / float(verified)))
    print("Number of Indian               : %6d %4.1f%%" % (indian, indian * 100 / float(verified)))
    print("Number of Asian                : %6d %4.1f%%" % (asian, asian * 100 / float(verified)))
    print("Number of Mixed                : %6d %4.1f%%" % (mixed, mixed * 100 / float(verified)))
    print("Number of Other                : %6d %4.1f%%" % (other, other * 100 / float(verified)))
    print("Number of active profiles (1m) : %6d %4.1f%%" % (active, active * 100 / float(verified)))
    print("Number of messages (1m)        : %6d" % (messages))
    print("Most blocked members           :", most_blocked)
    print("Most favorite members          :", most_favorite)
