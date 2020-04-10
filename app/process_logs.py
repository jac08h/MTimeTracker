import logging
from typing import List
import datetime as dt
import re
from pathlib import Path

from app.TimeLog import TimeLog

logger = logging.getLogger(__name__)

times_pattern = re.compile(r"(\d?\d):(\d?\d)")
categories_pattern = re.compile(r"([a-z]+)")


class InvalidTimelogError(Exception):
    pass


def get_time_logs_from_logfile(date: dt.date, logs_directory: str) -> List[TimeLog]:
    # construct filename
    logs_directory = Path(logs_directory)
    filename = logs_directory / date.strftime("%d_%m_%y.txt")
    time_logs = []
    with open(filename) as log:
        for line in log.readlines():
            try:
                times = re.findall(times_pattern, line)
                start_hour, start_minute = [int(i) for i in times[0]]
                end_hour, end_minute = [int(i) for i in times[1]]
                start_time = dt.time(hour=start_hour, minute=start_minute)
                end_time = dt.time(hour=end_hour, minute=end_minute)

                categories = re.findall(categories_pattern, line)
                if len(categories) == 0:
                    logger.error(f"{filename}: Invalid logfile entry: [{line}]. Exiting.")
                    raise InvalidTimelogError

                new_time_log = TimeLog(date=date, start=start_time, end=end_time, categories=categories)
                time_logs.append(new_time_log)

            except IndexError:
                stripped_line = re.sub(r"\s+", "", line, flags=re.UNICODE)
                if len(stripped_line) != 0:  # don't crash at empty lines
                    logger.error(f"{filename}: Invalid logfile entry: [{line}]. Exiting.")
                    raise InvalidTimelogError

    return time_logs


if __name__ == '__main__':
    d = dt.date(year=2020, month=1, day=2)
    logs = get_time_logs_from_logfile(d, '../test_logs')
    print(logs)
