from typing import Iterator
import datetime as dt
from dataclasses import dataclass

@dataclass
class DateRangeContainer:
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