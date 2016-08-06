
from datetime import datetime
from dateutil import tz
from email.utils import formatdate
from calendar import timegm
from youngs_server.youngs_app import log
from config.default import Config
# Hardcode zones:

from_zone = tz.gettz(Config.UTC_FROM)
to_zone = tz.gettz(Config.UTC_ZONE)


def today_obj():
    """ return today's date object """
    today_date = datetime.today().replace(tzinfo=from_zone).astimezone(to_zone).date()
    return today_date


def today_str():
    """ return today's date string """
    today_date = datetime.today().replace(tzinfo=from_zone).astimezone(to_zone).date()
    today_str = today_date.strftime("%m/%d/%Y")
    log.info('now datetime'+ str(datetime.today().replace(tzinfo=from_zone).astimezone(to_zone)))

    return today_str


def now_datetime():
    """ return now datetime object """
    now_datetime = datetime.today().replace(tzinfo=from_zone).astimezone(to_zone)
    return now_datetime


def str_to_datetime(datetime_str):
    """ dump string of today's datetime to datetime object"""

    if len(datetime_str) <= 10:
        # cast date to datetime
        result_datetime = datetime.strptime(datetime_str, "%m/%d/%Y")
    else:
        result_datetime = datetime.strptime(datetime_str, "%m/%d/%Y %H:%M")
    if result_datetime is None:
        log.info(result_datetime)
    return result_datetime


def str_to_date(date_str):
    """ dump string of today's date to date object"""
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").date()
    except:
        return None


def str_to_time(time_str):
    """ dump string of today's time to time object"""
    try:
        return datetime.strptime(time_str, "%H:%M").time()
    except:
        return None

def dump_datetime(value):
    if value is None:
        return None
    return value.strftime("%m/%d/%Y %H:%M")

def dump_date(value):
    if value is None:
        return None
    return value.strftime("%m/%d/%Y")
def dump_time(value):
    if value is None:
        return None
    return value.strftime("%H:%M")

def datetime_to_rfc822(dt):
    """
    See :func:`email.utils.formatdate` for more info on the RFC 822 format.

    :param dt: datetime
    :return: rfc822 formatted timestamp
    """
    if dt is None:
        return None
    return formatdate(timegm(dt.utctimetuple()))
