import pytest
import datetime as dt

from app.LogsProcessor import LogsProcessor
from app.helpers import get_date_range
from app.exceptions import *
from app.TimeLog import TimeLog

dummy_daterange = get_date_range(dt.date.today(), dt.date.today())
dummy_directory = 'asdf'
dummy_date = dt.date.today()
logs_processor = LogsProcessor(dummy_daterange, dummy_directory)


class TestProcessLogLinesCorrect:
    def test_bunch_of_correct_lines(self):
        lines_and_representations = {
            "10:12 - 10:40 - programming": (dt.time(hour=10, minute=12), dt.time(hour=10, minute=40), ['programming']),
            "09:21 - 13:12 - running, exercise": (
                dt.time(hour=9, minute=21), dt.time(hour=13, minute=12), ['running', 'exercise']),
            "21:12 - 22:42 . programming": (dt.time(hour=21, minute=12), dt.time(hour=22, minute=42), ['programming'])
        }
        for line, representation in lines_and_representations.items():
            assert logs_processor.process_logfile_line(line) == representation


def _test_incorrect_lines(lines: list, expected_exception):
    for line in lines:
        with pytest.raises(expected_exception) as excinfo:
            logs_processor.process_logfile_line(line)


class TestProcessLogLinesIncorrect:
    def test_hogwash(self):
        lines = [
            "falkdsj",
            "12:90832f;lkjdsa",
            "duhduh"
        ]
        _test_incorrect_lines(lines, BadLineError)

    def test_missing_activity(self):
        lines = [
            "18:00 - 18:01 - "
        ]
        _test_incorrect_lines(lines, BadLineError)

    def test_missing_time(self):
        lines = [
            "18:00 - a"
        ]
        _test_incorrect_lines(lines, BadLineError)

    def test_empty_lines(self):
        lines = [
            "",
            " ",
            "\n"
        ]
        _test_incorrect_lines(lines, EmptyLineError)

    def test_invalid_times(self):
        lines = [
            "24:12 - 24:58 - a",
            "12:65 - 12:85 - a",
        ]
        _test_incorrect_lines(lines, InvalidTimeError)

    def test_zero_duration(self):
        lines = [
            "13:12 - 13:12 - a",
            "12:04 - 12:04 - a"
        ]

        for line in lines:
            start, end, categories = logs_processor.process_logfile_line(line)
            with pytest.raises(LessThanMinimalDurationError):
                start = dt.datetime.combine(dummy_date, start)
                end = dt.datetime.combine(dummy_date, end)
                timelog = TimeLog(dummy_date, start, end, categories)

    def test_negative_duration(self):
        lines = [
            "13:12 - 13:00 - a",
            "12:04 - 12:03 - a"
        ]
        for line in lines:
            start, end, categories = logs_processor.process_logfile_line(line)
            with pytest.raises(LessThanMinimalDurationError):
                start = dt.datetime.combine(dummy_date, start)
                end = dt.datetime.combine(dummy_date, end)
                timelog = TimeLog(dummy_date, start, end, categories)
