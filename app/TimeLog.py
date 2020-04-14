import datetime as dt
from typing import List
from app.exceptions import LessThanMinimalDurationError


class TimeLog:
    def __init__(self, date: dt.date, start: dt.datetime, end: dt.datetime, categories: List[str]):
        self.date = date
        self.start = start
        self.end = end
        self.categories = sorted(categories)
        self.duration = self.calculate_duration()

    def calculate_duration(self) -> dt.timedelta:
        """
        Sets `self.duration` attribute.

        Raises NegativeDurationError.
        """
        duration = self.end - self.start
        min_duration = dt.timedelta(minutes=1)
        if duration < min_duration:
            raise LessThanMinimalDurationError
        return duration

    def __repr__(self):
        return f"{str(self.start)[:-3]} - {str(self.end)[:-3]} - " \
               f"{', '.join(self.categories)}  " \
               f"({str(self.duration)[:-3]})"

    def __eq__(self, other):
        return self.date == other.date and self.start == other.start \
               and self.end == other.end and self.categories == other.categories
