import logging
from typing import List, Tuple
import datetime as dt
import re
from pathlib import Path
from app.exceptions import *

from app.TimeLog import TimeLog
from app.DateRangeContainer import DateRangeContainer

logger = logging.getLogger(__name__)

times_pattern = re.compile(r"(\d?\d):(\d?\d)")
categories_pattern = re.compile(r"([a-z]+)")


class LogsProcessor:
    def __init__(self, daterange_container: DateRangeContainer, logs_directory: str):
        self.title = daterange_container.title
        self.daterange = daterange_container.daterange
        self.logs_directory = logs_directory

    def get_timelogs_from_date(self, date: dt.date) -> List[TimeLog]:
        """
        Raises:
            InvalidTimeLogError
            FileNotFoundError
        """
        filename = self.get_filename(date)
        time_logs = []
        with open(filename) as log:
            for line in log.readlines():
                try:
                    start_time, end_time, categories = self.process_logfile_line(line)
                    new_time_log = TimeLog(date=date, start=dt.datetime.combine(date, start_time),
                                           end=dt.datetime.combine(date, end_time), categories=categories)
                    time_logs.append(new_time_log)
                except BadLineError:
                    logger.error(f"{filename}: Invalid logfile entry: [{line}]. Exiting.")
                    raise InvalidTimelogError
                except EmptyLineError:
                    pass

        return time_logs

    def get_filename(self, date: dt.date) -> str:
        logs_directory = Path(self.logs_directory)
        filename = logs_directory / date.strftime("%d_%m_%y.txt")
        return filename

    def process_logfile_line(self, line: str) -> Tuple[dt.time, dt.time, List[str]]:
        """
        Returns:
             tuple containing start_time, end_time and categories

        Raises:
             BadLineError - Generic line error
             EmptyLineError
        """
        try:
            times = re.findall(times_pattern, line)
            start_hour, start_minute = [int(i) for i in times[0]]
            end_hour, end_minute = [int(i) for i in times[1]]
            start_time = dt.time(hour=start_hour, minute=start_minute)
            end_time = dt.time(hour=end_hour, minute=end_minute)
            categories = re.findall(categories_pattern, line)
            if len(categories) > 0:
                return start_time, end_time, categories
            else:
                raise BadLineError
        except IndexError:
            stripped_line = re.sub(r"\s+", "", line, flags=re.UNICODE)
            if len(stripped_line) == 0:
                raise EmptyLineError
            else:
                raise BadLineError

    def get_timelogs(self) -> List[TimeLog]:
        all_logs = []
        logs_processed = 0
        for date in self.daterange:
            try:
                new_logs = self.get_timelogs_from_date(date)
                all_logs += new_logs
                logs_processed += 1
            except FileNotFoundError:
                pass

        logger.info(f"Number of logs processed: {logs_processed}")
        return all_logs
