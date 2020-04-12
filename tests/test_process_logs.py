import pytest
import datetime as dt

from app.process_logs import LogsProcessor, InvalidTimelogError
from app.helpers import get_date_range
from app.TimeLog import TimeLog


class TestProcessLogsCorrect:
    def test_basic(self):
        date = dt.date(2020, 1, 1)
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/correct')
        extracted_logs = logs_processor.get_timelogs()

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
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/correct')
        extracted_logs = logs_processor.get_timelogs()

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
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/correct')
        extracted_logs = logs_processor.get_timelogs()

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
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/incorrect')
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = logs_processor.get_timelogs()

    def test_missing_activity(self):
        date = dt.date(2021, 1, 2)
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/incorrect')
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = logs_processor.get_timelogs()

    def test_missing_time(self):
        date = dt.date(2021, 1, 3)
        daterange = get_date_range(date, date)
        logs_processor = LogsProcessor(daterange, 'test_logs/incorrect')
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = logs_processor.get_timelogs()
