import pytest
import datetime as dt
from typing import List

from app.LogsProcessor import LogsProcessor
from app.helpers import get_date_range
from app.TimeLog import TimeLog
from app.exceptions import InvalidTimelogError


def create_and_run_log_processor_on_single_date(date: dt.date, directory: str) -> List[TimeLog]:
    daterange = get_date_range(date, date)
    logs_processor = LogsProcessor(daterange, directory)
    extracted_logs = logs_processor.get_timelogs_from_date(date)
    return extracted_logs


def run_incorrect(date):
    create_and_run_log_processor_on_single_date(date, 'test_logs/incorrect')


def run_correct(date) -> List[TimeLog]:
    return create_and_run_log_processor_on_single_date(date, 'test_logs/correct')


class TestProcessLogsCorrect:
    def test_basic(self):
        date = dt.date(2020, 1, 1)
        extracted_logs = run_correct(date)

        first_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=8, minute=0)),
                            end=dt.datetime.combine(date, dt.time(hour=9, minute=1)),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=13, minute=11)),
                             end=dt.datetime.combine(date, dt.time(hour=13, minute=42)),
                             categories=['school', 'math'])

        correct_logs = [first_log, second_log]
        assert correct_logs == extracted_logs

    def test_different_separators(self):
        date = dt.date(2020, 1, 2)
        extracted_logs = run_correct(date)

        first_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=8, minute=0)),
                            end=dt.datetime.combine(date, dt.time(hour=9, minute=1)),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=13, minute=11)),
                             end=dt.datetime.combine(date, dt.time(hour=13, minute=42)),
                             categories=['school', 'math'])
        third_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=13, minute=40)),
                            end=dt.datetime.combine(date, dt.time(hour=14, minute=58)),
                            categories=['exercise', 'run'])
        correct_logs = [first_log, second_log, third_log]
        assert correct_logs == extracted_logs

    def test_with_newline(self):
        date = dt.date(2020, 1, 3)
        extracted_logs = run_correct(date)

        first_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=8, minute=0)),
                            end=dt.datetime.combine(date, dt.time(hour=9, minute=1)),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.datetime.combine(date, dt.time(hour=13, minute=11)),
                             end=dt.datetime.combine(date, dt.time(hour=13, minute=42)),
                             categories=['school', 'math'])

        correct_logs = [first_log, second_log]
        assert correct_logs == extracted_logs


class TestProcessLogsIncorrect:

    def test_hogwash(self):
        date = dt.date(2021, 1, 1)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

    def test_missing_activity(self):
        date = dt.date(2021, 1, 2)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

    def test_missing_time(self):
        date = dt.date(2021, 1, 3)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

    def test_zero_minutes_duration(self):
        date = dt.date(2021, 1, 4)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

    def test_negative_duration(self):
        date = dt.date(2021, 1, 5)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

    def test_invalid_time(self):
        date = dt.date(2021, 1, 6)
        with pytest.raises(InvalidTimelogError) as excinfo:
            run_incorrect(date)

