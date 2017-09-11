from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import json
import sys
from collections import OrderedDict
from traceback import print_exc

from .parser import parse
from .parser import ParseError

ALFRED_TIME_FORMATS = (
    'to_datetime_string',
    'isoformat',
    'to_date_string',
    'to_time_string',
    'to_formatted_date_string',
    'to_rfc2822_string',
)


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
        time = parse(query)
    except ParseError as error:
        print_exc()
        return alfredify_error(error)

    if time is None:
        return [{'title': 'Continue typing...', 'valid': False}]

    formatted = apply_formats(time)
    return alfredify_times(formatted)


def main():
    output = {
        'items': generate_items(sys.argv[1:]),
    }
    print(json.dumps(output))


if __name__ == '__main__':
    sys.exit(main())
