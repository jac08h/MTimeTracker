import pandas as pd
import plotly.graph_objects as go
import logging
import datetime as dt
from typing import List

from app.exceptions import InvalidTimeUnitError

logger = logging.getLogger(__name__)


class TimelogsDataframe:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def bar_plot(self, time_unit='minutes'):
        """
        Display simple bar plot
        """
        fig = go.Figure([go.Bar(x=self.df['date'],
                                y=self.df['duration'].dt.total_seconds() / self.timeunit_to_seconds(time_unit),
                                text=self.df['categories'],
                                textposition='auto',
                                hovertext=self.df['time_start'].dt.strftime('%H:%M')
                                )])
        fig.show()

    def timeunit_to_seconds(self, time_unit: str) -> int:
        if time_unit in ['seconds', 'sec', 's']:
            return 1
        elif time_unit in ['minutes', 'min', 'm']:
            return 60
        elif time_unit in ['hours', 'h']:
            return 3600
        elif time_unit in ['days', 'd']:
            return 86400
        else:
            raise InvalidTimeUnitError

    def filter_by_categories(self, categories: List[str]) -> pd.DataFrame:
        """
        Return a dataframe with logs containing all specified categories
        """
        contains_all_mask = self.df['categories'].apply(lambda x: cat in x for cat in categories)
        return self.df[contains_all_mask]

    def get_total_time(self) -> dt.timedelta:
        """
        Total amount of tracked time
        """
        return self.df.duration.sum()

    def get_time_in_categories(self, categories: List[str]) -> dt.timedelta:
        """
        Amount of time in specified categories
        """
        filtered_df = self.filter_by_categories(categories)
        return filtered_df.duration.sum()
