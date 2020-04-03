import argparse
from typing import Dict, Iterator
import datetime as dt
import logging

logger = logging.getLogger(__name__)


def daterange(date_a: dt.date, date_b: dt.date) -> Iterator[dt.date]:
    """
    Return iterator of iterative range of dates between the arguments
    """
    one_day = dt.timedelta(days=1)
    current = date_a
    while current <= date_b:
        yield current
        current += one_day


def get_last_monday(date: dt.date) -> dt.date:
    """
    Return the date of last Monday
    """
    last_mon = date - dt.timedelta(days=date.weekday())
    return last_mon


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='Directory containing text files with logged activities')
    parser.add_argument('-sd', '--start_date', type=str, help='Date in DD-MM-YYYY format')
    parser.add_argument('-ed', '--end_date', type=str, help='Date in  DD-MM-YYYY format')
    parser.add_argument('-t', '--today', help='Today', action='store_true')
    parser.add_argument('-ty', '--this_year', help='This year', action='store_true')
    parser.add_argument('-tm', '--this_month', help='This month', action='store_true')
    parser.add_argument('-tw', '--this_week', help='This week', action='store_true')

    return parser.parse_args()


def process_date_args(args: argparse.Namespace) -> Dict:
    """
    Return a dictionary containing
        iterator of dates to process and
        title
    """
    d = {'range': None, 'title': None}
    if args.today:
        today = dt.date.today()
        d['range'] = daterange(today, today)
        d['title'] = 'Today'

    elif args.this_week:
        today = dt.date.today()
        last_monday = get_last_monday(today)
        d['range'] = daterange(last_monday, today)
        d['title'] = 'This Week'

    elif args.this_month:
        today = dt.date.today()
        first_in_month = dt.date(year=today.year, month=today.month, day=1)
        d['range'] = daterange(first_in_month, today)
        d['title'] = 'This Month'

    elif args.this_year:
        today = dt.date.today()
        first_in_year = dt.date(year=today.year, month=1, day=1)
        d['range'] = daterange(first_in_year, today)
        d['title'] = 'This Year'

    elif args.start_date:
        day, month, year = [int(i) for i in args.start_date.split('-')]
        start_date = dt.date(year, month, day)
        if args.end_date:
            day, month, year = [int(i) for i in args.end_date.split('-')]
            end_date = dt.date(year, month, day)
            d['range'] = daterange(start_date, end_date)
            d['title'] = f"{args.start_date} -> {args.end_date}"

        else:
            d['range'] = daterange(start_date, start_date)
            d['title'] = args.start_date

    else:
        logger.error('Invalid arguments. See -h for usage.')

    return d


def main():
    args = get_args()
    d = process_date_args(args)


if __name__ == '__main__':
    main()
