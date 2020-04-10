import argparse
from typing import Iterator
import datetime as dt
import logging
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

CURRENT_MILLENIUM = 2000
date_pattern = re.compile(r"(\d\d).(\d\d).(\d\d)")


@dataclass
class DateRange:
    title: str
    daterange: Iterator[dt.date]


def empty_iterator() -> Iterator[None]:
    yield from ()


def get_date_range(date_a: dt.date, date_b: dt.date) -> Iterator[dt.date]:
    one_day = dt.timedelta(days=1)
    current = date_a
    while current <= date_b:
        yield current
        current += one_day


def get_last_monday(date: dt.date) -> dt.date:
    last_mon = date - dt.timedelta(days=date.weekday())
    return last_mon


def get_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-sd', '--start_date', type=str, help='Date in DD-MM-YY format')
    parser.add_argument('-ed', '--end_date', type=str, help='Date in  DD-MM-YY format')
    parser.add_argument('-t', '--today', help='Today', action='store_true')
    parser.add_argument('-ty', '--this_year', help='This year', action='store_true')
    parser.add_argument('-tm', '--this_month', help='This month', action='store_true')
    parser.add_argument('-tw', '--this_week', help='This week', action='store_true')
    parser.add_argument('directory', type=str, help='Directory containing text files with logged activities')

    return parser.parse_args(args)


def process_date_args(args: argparse.Namespace) -> DateRange:
    today = dt.date.today()
    if args.today:
        daterange_from_args = DateRange(title='Today', daterange=get_date_range(today, today))

    elif args.this_week:
        last_monday = get_last_monday(today)
        daterange_from_args = DateRange(title='This Week', daterange=get_date_range(last_monday, today))

    elif args.this_month:
        first_in_month = dt.date(year=today.year, month=today.month, day=1)
        daterange_from_args = DateRange(title='This Month', daterange=get_date_range(first_in_month, today))

    elif args.this_year:
        first_in_year = dt.date(year=today.year, month=1, day=1)
        daterange_from_args = DateRange(title='This Year', daterange=get_date_range(first_in_year, today))

    elif args.start_date:
        extracted_numbers = re.findall(date_pattern, args.start_date)
        day, month, year_last_two_digits = [int(i) for i in extracted_numbers[0]]
        year = CURRENT_MILLENIUM + year_last_two_digits
        start_date = dt.date(year, month, day)

        if args.end_date:
            extracted_numbers = re.findall(date_pattern, args.end_date)
            day, month, year_last_two_digits = [int(i) for i in extracted_numbers[0]]
            year = CURRENT_MILLENIUM + year_last_two_digits
            end_date = dt.date(year, month, day)
            daterange_from_args = DateRange(
                title=f"{start_date.strftime('%d-%m-%y')} -> {end_date.strftime('%d-%m-%y')}",
                daterange=get_date_range(start_date, end_date))

        else:
            daterange_from_args = DateRange(title=start_date.strftime('%d-%m-%y'),
                                            daterange=get_date_range(start_date, start_date))

    else:
        logger.error('Invalid arguments. See -h for usage.')
        exit()

    return daterange_from_args
