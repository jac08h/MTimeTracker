from typing import List
import datetime as dt
import re
from TimeLog import TimeLog

CATEGORIES_DELIMETER = '-'
times_pattern = re.compile(r"(\d?\d):(\d?\d)")
categories_pattern = re.compile(r"([a-z]+)")


def read_logfile(filename: str) -> List[TimeLog]:
    time_logs = []
    with open(filename) as log:
        for line in log.readlines():
            times = re.findall(times_pattern, line)
            start_hour, start_minute = [int(i) for i in times[0]]
            end_hour, end_minute = [int(i) for i in times[1]]
            start_time = dt.time(hour=start_hour, minute=start_minute)
            end_time = dt.time(hour=end_hour, minute=end_minute)

            categories = re.findall(categories_pattern, line)  # allows for 0 categories
            new_time_log = TimeLog(start=start_time, end=end_time, categories=categories)
            time_logs.append(new_time_log)

    return time_logs


if __name__ == '__main__':
    logs = read_logfile('../time_logs/03_04_2020.txt')
    for log in logs:
        print(log)
