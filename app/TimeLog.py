import datetime as dt
from typing import List


class TimeLog:
    def __init__(self, date: dt.date, start: dt.time, end: dt.time, categories: List[str]):
        self.date = date
        self.start = start
        self.end = end
        self.categories = sorted(categories)
        self.duration = time_diff(start, end)

    def __repr__(self):
        return f"{str(self.start)[:-3]} - {str(self.end)[:-3]} - " \
               f"{', '.join(self.categories)}  " \
               f"({str(self.duration)[:-3]})"

    def __eq__(self, other):
        return self.date == other.date and self.start == other.start \
               and self.end == other.end and self.categories == other.categories


def time_diff(start: dt.time, end: dt.time) -> dt.time:
    """
    Calculate difference between two times.

    Assumes the times are from the same day.
    Raises ValueError if end represents earlier time than start.
    """
    diff_hour = end.hour - start.hour
    if end.minute >= start.minute:
        diff_minute = end.minute - start.minute
    else:
        diff_hour -= 1
        diff_minute = (60 - start.minute) + end.minute

    diff_time = dt.time(hour=diff_hour, minute=diff_minute)
    return diff_time
