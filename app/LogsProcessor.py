import logging
from typing import List, Tuple, Iterator
import datetime as dt
import re
from pathlib import Path
import pandas as pd

from app.TimeLog import TimeLog
from app.exceptions import *

logger = logging.getLogger(__name__)

times_pattern = re.compile(r"(\d?\d):(\d?\d)")
categories_pattern = re.compile(r"([A-Za-z]+)")


class LogsProcessor:
    def __init__(self, daterange: Iterator[dt.date], logs_directory: str):
        self.daterange = daterange
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
                except EmptyLineError:
                    pass
                except LessThanMinimalDurationError:
                    self.log_line_error('Invalid duration', line, filename)
                    raise InvalidTimelogError
                except InvalidTimeError:
                    self.log_line_error('Invalid time', line, filename)
                    raise InvalidTimelogError
                except BadLineError:
                    self.log_line_error('Invalid log file entry', line, filename)
                    raise InvalidTimelogError

        return time_logs

    def log_line_error(self, msg: str, line: str, filename: str):
        logger.error(f"{msg}: `{line.strip()}`  ({filename})")

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
             InvalidTimeError
             EmptyLineError
        """
        try:
            times = re.findall(times_pattern, line)
            start_hour, start_minute = [int(i) for i in times[0]]
            end_hour, end_minute = [int(i) for i in times[1]]
            try:
                start_time = dt.time(hour=start_hour, minute=start_minute)
                end_time = dt.time(hour=end_hour, minute=end_minute)
            except ValueError:
                raise InvalidTimeError

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
        logs_correct = 0
        logs_invalid = 0
        for date in self.daterange:
            try:
                new_logs = self.get_timelogs_from_date(date)
                all_logs += new_logs
                logs_correct += 1
            except FileNotFoundError:
                pass
            except InvalidTimelogError:
                logs_invalid += 1

        logger.info(f"Correct logs: {logs_correct}  Invalid logs: {logs_invalid}")
        return all_logs

    def create_df(self, logs: List[TimeLog]) -> pd.DataFrame:
        columns = ['date', 'time_start', 'time_end', 'categories', 'duration']

        logs_list_for_df = []
        for log in logs:
            logs_list_for_df.append([log.date, log.start, log.end, ','.join(log.categories), log.duration])

        logs_df = pd.DataFrame(logs_list_for_df, columns=columns)
        logs_df['date'] = pd.to_datetime(logs_df['date'])
        # time_start and time_end are converted to datetime implicitly, so is duration to timedelta

        return logs_df
