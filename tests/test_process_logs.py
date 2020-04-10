import pytest
import datetime as dt

from app.process_logs import get_time_logs_from_logfile, InvalidTimelogError
from app.TimeLog import TimeLog


class TestProcessLogsCorrect:
    def test_basic(self):
        date = dt.date(2020, 1, 1)
        extracted_logs = get_time_logs_from_logfile(date, 'test_logs/correct')

        first_log = TimeLog(date, start=dt.time(hour=8, minute=0), end=dt.time(hour=9, minute=1),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.time(hour=13, minute=11), end=dt.time(hour=13, minute=42),
                             categories=['school', 'math'])

        correct_logs = [first_log, second_log]
        assert correct_logs == extracted_logs

    def test_different_separators(self):
        date = dt.date(2020, 1, 2)
        extracted_logs = get_time_logs_from_logfile(date, 'test_logs/correct')
        first_log = TimeLog(date, start=dt.time(hour=8, minute=0), end=dt.time(hour=9, minute=1),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.time(hour=13, minute=11), end=dt.time(hour=13, minute=42),
                             categories=['school', 'math'])
        third_log = TimeLog(date, start=dt.time(hour=13, minute=40), end=dt.time(hour=14, minute=58),
                            categories=['exercise', 'run'])

        correct_logs = [first_log, second_log, third_log]
        assert correct_logs == extracted_logs

    def test_with_newline(self):
        date = dt.date(2020, 1, 3)
        extracted_logs = get_time_logs_from_logfile(date, 'test_logs/correct')
        first_log = TimeLog(date, start=dt.time(hour=8, minute=0), end=dt.time(hour=9, minute=1),
                            categories=['programming', 'personal'])
        second_log = TimeLog(date, start=dt.time(hour=13, minute=11), end=dt.time(hour=13, minute=42),
                             categories=['school', 'math'])

        correct_logs = [first_log, second_log]
        assert correct_logs == extracted_logs


class TestProcessLogsIncorrect:
    def test_hogwash(self):
        date = dt.date(2021, 1, 1)
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = get_time_logs_from_logfile(date, 'test_logs/incorrect')

    def test_missing_activity(self):
        date = dt.date(2021, 1, 2)
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = get_time_logs_from_logfile(date, 'test_logs/incorrect')

    def test_missing_time(self):
        date = dt.date(2021, 1, 3)
        with pytest.raises(InvalidTimelogError) as excinfo:
            extracted_logs = get_time_logs_from_logfile(date, 'test_logs/incorrect')
