import datetime as dt
from app.parse_cl_args import process_date_args, get_args

today = dt.date.today()


class TestToday:
    args = get_args(['--today', 'tmp'])

    def test_today(self):
        dates_data = process_date_args(self.args)
        list_daterange = list(dates_data.daterange)

        assert dates_data.title == 'Today'
        assert today in list_daterange
        assert len(list_daterange) == 1


class TestThisWeek:
    args = get_args(['--this_week', 'tmp'])

    def test_this_week(self):
        dates_data = process_date_args(self.args)
        list_daterange = list(dates_data.daterange)
        assert dates_data.title == 'This Week'
        assert today in list_daterange
        assert len(list_daterange) == (today.weekday() + 1)


class TestThisMonth:
    args = get_args(['--this_month', 'tmp'])

    def test_this_month(self):
        dates_data = process_date_args(self.args)
        list_daterange = list(dates_data.daterange)
        assert dates_data.title == 'This Month'
        assert today in list_daterange
        assert len(list_daterange) == today.day


class TestThisYear:
    args = get_args(['--this_year', 'tmp'])

    def test_this_month(self):
        dates_data = process_date_args(self.args)
        list_daterange = list(dates_data.daterange)
        first_in_year = dt.date(year=today.year, month=1, day=1)
        seconds_elapsed = (today - first_in_year).total_seconds()
        days_elapsed = seconds_elapsed / 86400
        assert dates_data.title == 'This Year'
        assert today in list_daterange
        assert len(list_daterange) == days_elapsed+1

