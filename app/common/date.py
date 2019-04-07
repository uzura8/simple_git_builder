import datetime

def validate_date(value, date_format='%Y-%m-%d'):
    try:
        datetime.datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False
