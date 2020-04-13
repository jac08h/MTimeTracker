from typing import Iterator
import datetime as dt
from dataclasses import dataclass


@dataclass
class DateRangeContainer:
    title: str
    daterange: Iterator[dt.date]
