import json
import sys
from collections import OrderedDict
from traceback import print_exc

import pendulum
from pendulum.parsing.exceptions import ParserError

ALFRED_TIME_FORMATS = (
    'to_datetime_string',
    'isoformat',
    'to_date_string',
    'to_time_string',
    'to_formatted_date_string',
    'to_rfc2822_string',
)
# Use OrderedDict so there a priority to partial matches
TIME_STRINGS = OrderedDict({
    'now': pendulum.now,
    'today': pendulum.today,
    'tomorrow': pendulum.tomorrow,
    'yesterday': pendulum.yesterday,
    'monday': lambda: day_of_week(pendulum.MONDAY),
    'tuesday': lambda: day_of_week(pendulum.TUESDAY),
    'wednesday': lambda: day_of_week(pendulum.WEDNESDAY),
    'thursday': lambda: day_of_week(pendulum.THURSDAY),
    'friday': lambda: day_of_week(pendulum.FRIDAY),
    'saturday': lambda: day_of_week(pendulum.SATURDAY),
    'sunday': lambda: day_of_week(pendulum.SUNDAY),
})


def day_of_week(day_of_week):
    today = pendulum.today()
    if today.day_of_week == day_of_week:
        return today
    return today.next(day_of_week)


def parse_time(query):
    query = ' '.join(query)
    for time_string, time in TIME_STRINGS.items():
        if time_string.startswith(query.lower()):
            return time()
    try:
        return pendulum.from_timestamp(int(query))
    except ValueError:
        return pendulum.parse(query)


def apply_formats(time, formats=ALFRED_TIME_FORMATS):
    formats = OrderedDict()
    for time_format in ALFRED_TIME_FORMATS:
        func = getattr(time, time_format, None)
        if func:
            formats[time_format] = func()
        else:
            formats[time_format] = time.format(time_format)

    return formats


def alfredify_times(times_formatted):
    return [
        {
            'uid': time_format,
            'title': formatted,
            'subtitle': time_format,
            'arg': formatted,
        }
        for time_format, formatted in times_formatted.items()
    ]


def alfredify_error(error):
    return [{
        'title': error.args[0],
        'valid': False,
    }]


def generate_items(query):
    try:
        time = parse_time(query)
    except ParserError as error:
        print_exc()
        return alfredify_error(error)

    formatted = apply_formats(time)
    return alfredify_times(formatted)


def main():
    output = {
        'items': generate_items(sys.argv[1:]),
    }
    print(json.dumps(output))


if __name__ == '__main__':
    sys.exit(main())
