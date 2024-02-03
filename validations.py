import re
from datetime import datetime


def is_valid_time_format(input_str):
    time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
    return bool(re.match(time_pattern, input_str))


def is_valid_date_format(input_str):
        try:
            datetime_object = datetime.strptime(input_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False


def is_empty_string(input_str):
    if input_str == '':
        return False
    else:
        return True


def reserved_sold(input_str):
    if input_str == 'reserved' or input_str == 'sold':
        return True
    else:
        return False


def is_valid_day_of_week(day_str):
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    return day_str.lower() in valid_days
