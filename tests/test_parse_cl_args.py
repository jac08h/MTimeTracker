import datetime as dt
from app.parse_cl_args import daterange_from_cl_args, get_args

today = dt.date.today()


class TestToday:
    args = get_args(['--today', 'tmp'])

    def test_today(self):
        daterange = daterange_from_cl_args(self.args)
        list_daterange = list(daterange)

        assert today in list_daterange
        assert len(list_daterange) == 1


class TestThisWeek:
    args = get_args(['--this_week', 'tmp'])

    def test_this_week(self):
        daterange = daterange_from_cl_args(self.args)
        list_daterange = list(daterange)
        assert today in list_daterange
        assert len(list_daterange) == (today.weekday() + 1)


class TestThisMonth:
    args = get_args(['--this_month', 'tmp'])

    def test_this_month(self):
        daterange = daterange_from_cl_args(self.args)
        list_daterange = list(daterange)
        assert today in list_daterange
        assert len(list_daterange) == today.day


class TestThisYear:
    args = get_args(['--this_year', 'tmp'])

    def test_this_month(self):
        daterange = daterange_from_cl_args(self.args)
        list_daterange = list(daterange)
        first_in_year = dt.date(year=today.year, month=1, day=1)
        seconds_elapsed = (today - first_in_year).total_seconds()
        days_elapsed = seconds_elapsed / 86400
        assert today in list_daterange
        assert len(list_daterange) == days_elapsed+1

