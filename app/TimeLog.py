import datetime as dt
from typing import List


class TimeLog:
    def __init__(self, date: dt.date, start: dt.datetime, end: dt.datetime, categories: List[str]):
        self.date = date
        self.start = start
        self.end = end
        self.categories = sorted(categories)
        self.duration = end - start

    def __repr__(self):
        return f"{str(self.start)[:-3]} - {str(self.end)[:-3]} - " \
               f"{', '.join(self.categories)}  " \
               f"({str(self.duration)[:-3]})"

    def __eq__(self, other):
        return self.date == other.date and self.start == other.start \
               and self.end == other.end and self.categories == other.categories

