from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
from collections import OrderedDict
from traceback import print_exc

import pendulum
from pendulum.parsing.exceptions import ParserError
from pytzdata import get_timezones


TIMEZONES = tuple(tz.lower() for tz in get_timezones()) + ('local', 'utc')

# Use OrderedDict so there a priority to partial matches
TIME_STRINGS = OrderedDict({
    'now': pendulum.now,
    'today': pendulum.today,
    'tomorrow': pendulum.tomorrow,
    'yesterday': pendulum.yesterday,
    'utc': lambda: pendulum.now('UTC'),
})
DAYS_OF_WEEK = {
    'monday': pendulum.MONDAY,
    'tuesday': pendulum.TUESDAY,
    'wednesday': pendulum.WEDNESDAY,
    'thursday': pendulum.THURSDAY,
    'friday': pendulum.FRIDAY,
    'saturday': pendulum.SATURDAY,
    'sunday': pendulum.SUNDAY,
}
UNITS = {
    ('microseconds', 'microsecond', 'ms'): 'microseconds',
    ('seconds', 'second', 's'): 'seconds',
    ('minutes', 'minute', 'min'): 'minutes',
    ('hours', 'hour', 'hr'): 'hours',
    ('days', 'day', 'dy'): 'days',
    ('weeks', 'week', 'wk'): 'weeks',
    ('months', 'month', 'mn'): 'months',
    ('years', 'year', 'yr'): 'years',
}


class ParseError(Exception):
    pass


def parse_interval(query):
    interval_args = defaultdict(int)
    query_parts = iter(query.split())
    for part in query_parts:
        # TODO: Handle combined amount and unit eg. 2min
        amount = int(part)
        query = next(query_parts, None)
        if query is None:
            break

        for words, unit in UNITS.items():
            if query in words:
                interval_args[unit] += amount

    return interval_args


def parse_addition(query, time):
    add_args = parse_interval(query)
    return time.add(**add_args)


def parse_subtraction(query, time):
    sub_args = parse_interval(query)
    return time.subtract(**sub_args)


def parse_day_of_week(query):
    # If query is less than 2 then day of week can't be distinctly determined
    if len(query) < 2:
        return None

    for day, pendulum_day in DAYS_OF_WEEK.items():
        if day.startswith(query):
            return pendulum_day

    return None


def parse_next(query, time):
    day_of_week = parse_day_of_week(query)

    if day_of_week is None:
        return None

    return time.next(day_of_week)


def parse_previous(query, time):
    day_of_week = parse_day_of_week(query)

    if day_of_week is None:
        return None

    return time.previous(day_of_week)


def parse_start_of(query, time):
    try:
        return time.start_of(query)
    except ValueError:
        # TODO: Add error message
        return None


def parse_end_of(query, time):
    try:
        return time.end_of(query)
    except ValueError:
        # TODO: Add error message
        return None


def parse_to(query, time):
    if query not in TIMEZONES:
        match_tzs = [
            tz for tz in TIMEZONES
            if all((segment in tz) for segment in query.split())
        ]
        if len(match_tzs) == 1:
            query = match_tzs[0]
        else:
            return None
    return time.in_timezone(query)


PARSING_FUNCS = OrderedDict({
    '+': parse_addition,
    'add': parse_addition,
    'addition': parse_addition,
    '-': parse_subtraction,
    'sub': parse_subtraction,
    'subtract': parse_subtraction,
    'next': parse_next,
    'previous': parse_previous,
    'prev': parse_previous,
    'start of': parse_start_of,
    'start': parse_start_of,
    'end of': parse_end_of,
    'end': parse_end_of,
    'to': parse_to,
})


def day_of_week(day_of_week):
    today = pendulum.today()
    if today.day_of_week == day_of_week:
        return today
    return today.next(day_of_week)


def parse_time(query):
    for time_string, time in TIME_STRINGS.items():
        if time_string.startswith(query.lower()):
            return time()
    try:
        return pendulum.from_timestamp(float(query), 'local')
    except ValueError:
        pass

    try:
        return pendulum.parse(query)
    except ParserError as error:
        print_exc()
        raise ParseError(error.args[0])


def parse_segment(query, time):
    norm_query = query.strip().lower()
    for prefix, parsing_func in PARSING_FUNCS.items():
        if norm_query.startswith(prefix):
            if time is None:
                time = pendulum.now()

            no_prefix = norm_query[len(prefix):].strip()

            return parsing_func(no_prefix.lower(), time)

    if time is None:
        return parse_time(query)

    raise ParseError('Time string was not the first argument')


def is_timezone(segment, prev_segments):
    del segment, prev_segments
    return False


def parse(query):
    time = None
    segments = []

    for segment in query:
        if is_timezone(segment, segments):
            segments.append(segment)
            continue

        for prefix in PARSING_FUNCS:
            if segment.startswith(prefix):
                time = parse_segment(' '.join(segments), time)
                segments = [segment]
                break
        else:
            segments.append(segment)

    if segments:
        time = parse_segment(' '.join(segments), time)

    return time
