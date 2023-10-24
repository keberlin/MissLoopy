from localization import *
from mlemail import *
from mlhtml import *
from mllist import *
from mlutils import *

FROM = TITLE + "<noreply@" + DOMAIN + ">"

ADMIN_EMAIL = "keith.hollis@gmail.com"


def EmailNewPhoto(session, filename, pid, id):
    dict = {}
    dict["id"] = id
    # dict['image'] = ImageData(filename)
    dict["filename"] = filename

    html = RenderY("email-new-photo.html", dict)
    Email2(FROM, [ADMIN_EMAIL], "New Photo Uploaded (%d)" % (pid), html, 10)


def EmailVerify(session, email, uuid):
    dict = {}
    dict["uuid"] = uuid
    dict["email"] = email

    html = RenderY("email-verify.html", dict)
    Email2(FROM, [email], "Verify Registration", html, 1)


def EmailResetPassword(session, email, uuid):
    dict = {}
    dict["uuid"] = uuid
    dict["email"] = email

    html = RenderY("email-reset-password.html", dict)
    Email2(FROM, [email], "Password Reset Link", html, 1)


def EmailKicked(session, email):
    dict = {}

    html = RenderY("email-kicked.html", dict)
    Email2(FROM, [email], "Removal Alert", html)


def EmailKickedStopForumSpam(session, email):
    dict = {}

    html = RenderY("email-kicked-stopforumspam.html", dict)
    Email2(FROM, [email], "Removal Alert", html)


def EmailPhotoDeleted(session, email):
    dict = {}

    html = RenderY("email-photo-deleted.html", dict)
    Email2(FROM, [email], "Photo Removal Alert", html)


def EmailWink(session, entry, entry_from):
    email = entry.email
    location = entry.location
    country = GazCountry(location)
    tz = entry.tz
    adjust = GazLatAdjust(entry_from.y)
    dx = abs(entry_from.x - entry.x) * adjust / 1000
    dy = abs(entry_from.y - entry.y) / 1000
    distance = math.sqrt((dx * dx) + (dy * dy))

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    dict = {}
    dict["action"] = "emailthread"
    dict["navigation"] = "inbox"

    member = {}
    member["id"] = entry_from.id
    member["image"] = PhotoFilename(MasterPhoto(session, entry_from.id))
    member["name"] = mask.MaskEverything(entry_from.name)
    member["gender"] = Gender(entry_from.gender)
    member["age"] = Age(entry_from.dob)
    member["starsign"] = Starsign(entry_from.dob)
    member["ethnicity"] = Ethnicity(entry_from.ethnicity)
    member["location"] = entry_from.location
    member["summary"] = mask.MaskEverything(entry_from.summary)
    member["last_login"] = Since(entry_from.last_login)
    member["login_country"] = entry_from.last_ip_country
    member["created"] = Datetime(entry_from.created2, tz).strftime("%x")
    member["distance"] = Distance(distance, unit_distance)
    member["active"] = False
    dict["entry"] = member

    html = RenderY("email-wink.html", dict)
    Email2(FROM, [email], "New Wink! Received", html)


def EmailNotify(session, entry, entry_from):
    email = entry.email
    location = entry.location
    country = GazCountry(location)
    tz = entry.tz
    adjust = GazLatAdjust(entry_from.y)
    dx = abs(entry_from.x - entry.x) * adjust / 1000
    dy = abs(entry_from.y - entry.y) / 1000
    distance = math.sqrt((dx * dx) + (dy * dy))

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    dict = {}
    dict["action"] = "emailthread"
    dict["navigation"] = "inbox"

    member = {}
    member["id"] = entry_from.id
    member["image"] = PhotoFilename(MasterPhoto(session, entry_from.id))
    member["name"] = mask.MaskEverything(entry_from.name)
    member["gender"] = Gender(entry_from.gender)
    member["age"] = Age(entry_from.dob)
    member["starsign"] = Starsign(entry_from.dob)
    member["ethnicity"] = Ethnicity(entry_from.ethnicity)
    member["location"] = entry_from.location
    member["summary"] = mask.MaskEverything(entry_from.summary)
    member["last_login"] = Since(entry_from.last_login)
    member["login_country"] = entry_from.last_ip_country
    member["created"] = Datetime(entry_from.created2, tz).strftime("%x")
    member["distance"] = Distance(distance, unit_distance)
    member["active"] = False
    dict["entry"] = member

    html = RenderY("email-notify.html", dict)
    Email2(FROM, [email], "New Message Received", html)


def EmailNewMembers(session, entry, entries):
    email = entry.email
    location = entry.location
    country = GazCountry(location)
    x = entry.x
    y = entry.y
    tz = entry.tz

    SetLocale(country)

    unit_distance, unit_height = Units(country)

    dict = {}
    dict["action"] = "member"
    dict["navigation"] = "matches"
    dict["entries"] = ListMembers(session, entries, None, location, x, y, tz, unit_distance)

    html = RenderY("email-newmembers.html", dict)
    Email2(FROM, [email], "New Members Available", html, 4)


def EmailInboxReminder(session, email, name):
    dict = {}
    dict["name"] = name

    html = RenderY("email-inbox-reminder.html", dict)
    Email2(FROM, [email], "Unread Messages Reminder", html, 1)
