import datetime
import pandas as pd
import logging

from django.conf import settings

from .g_drive_modules import GoogleSheetReader

logger = logging.getLogger(__name__)


class SalaahTimeReader(GoogleSheetReader):
    def __init__(self, sheet_id, client_secret, token_cache, sheet_name='24 Hour', refresh_interval=300):
        super().__init__(sheet_id=sheet_id, client_secret=client_secret, token_cache=token_cache)
        self.SHEET_NAME = sheet_name
        self.CACHE = None
        self.refresh_interval = refresh_interval
        self._MASTER_DATES = None

    def _create_date(self, year, month, day):
        return datetime.date(year, int(month), int(day))

    def _update(self):
        self._MASTER_DATES = self.read_data_as_pd(sheet_name=self.SHEET_NAME)
        frames = []

        # Getting next 5 year of dates and last 3
        years = [datetime.date.today().year + i for i in range(5)]
        years += [datetime.date.today().year - i for i in range(1, 4)]
        for year in years:
            logger.info('Creating dates for: {}'.format(year))
            temp = self._MASTER_DATES.copy()
            temp['DATE'] = self._MASTER_DATES[['MONTH', 'DAY']].apply(lambda x: self._create_date(year ,*x), axis=1)
            temp['YEAR'] = year
            temp['DAYOFWEEK'] = temp['DATE'].apply(lambda x: x.strftime('%A'))
            temp['MONTH'] = self._MASTER_DATES.MONTH.apply(lambda x: int(x))
            temp['DAY'] = self._MASTER_DATES.DAY.apply(lambda x: int(x))
            frames.append(temp)

        self.CACHE = pd.concat(frames)

    def run(self):
        self._update()
        logger.info('Cached Updated')


config = settings.CONFIG.SalaahTimeReader
salaah_finder = SalaahTimeReader(sheet_id=config['sheet_id'],
                                 client_secret=config['client_secret'],
                                 token_cache=config['token_cache'],
                                 sheet_name=config['sheet_name'],
                                 refresh_interval=config['refresh_interval'])
salaah_finder.run()