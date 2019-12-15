import datetime
import pytz
import dateutil.parser


def datetime_now():
    return datetime.datetime.now().replace(tzinfo=pytz.utc)


def datetime_to_iso(dt: datetime):
    return dt.isoformat()


def iso_to_datetime(dt_str):
    return dateutil.parser.parse(dt_str)