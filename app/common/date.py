import datetime
import pytz
from pytz import timezone

def validate_date(value, date_format='%Y-%m-%d'):
    try:
        datetime.datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False


def conv_dt_from_utc(dt_value, timezone_str='', format='%Y/%m/%d %H:%M'):
    if not timezone_str:
        return

    utc_tz = pytz.timezone('UTC')
    utc_dt = utc_tz.localize(dt_value, is_dst=None).astimezone(pytz.utc)
    local_tz = pytz.timezone(timezone_str)
    local_dt = utc_dt.astimezone(local_tz)
    return local_dt.strftime(format)
