import pytz


def Datetime(dt, tz):
    return dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(tz))
