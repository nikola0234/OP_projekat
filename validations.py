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


def check_projection_overlap(projections, new_projection):
    new_hall = new_projection['cinema hall']
    new_start_time = datetime.strptime(new_projection['starting time'], '%H:%M')
    new_end_time = datetime.strptime(new_projection['ending time'], '%H:%M')
    new_days = new_projection['days'].split(', ')

    for projection in projections:
        if projection['cinema hall'] == new_hall:
            existing_start_time = datetime.strptime(projection['starting time'], '%H:%M')
            existing_end_time = datetime.strptime(projection['ending time'], '%H:%M')
            existing_days = projection['days'].split(', ')

            if any(day in new_days for day in existing_days):
                if (new_start_time < existing_end_time and new_end_time > existing_start_time):
                    return True

    return False
