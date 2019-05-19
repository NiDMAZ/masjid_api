import logging
import datetime
import threading
from datetime import timedelta
import time
from django.conf import settings

from .g_drive_modules import GoogleSheetReader
from .converters_formatter import string2date

logger = logging.getLogger(__name__)


class JummahKhateebReader(GoogleSheetReader):
    def __init__(self, sheet_id, client_secret, token_cache, sheet_name, refresh_interval):
        super().__init__(sheet_id=sheet_id, client_secret=client_secret, token_cache=token_cache)
        self.SHEET_NAME = sheet_name
        self.CACHE = None
        self.refresh_interval = refresh_interval

    def get_jummah_date(self, date_time=datetime.datetime.now()):
        assert type(date_time) == datetime.datetime, "Only accepts {}, received {}".format(datetime.datetime,
                                                                                           type(date_time))
        isoweekday = date_time.isoweekday()

        if isoweekday < 5:
            # print 'Its before Friday'
            delta = timedelta(days=5 - isoweekday)
            new_date = date_time + delta
            return new_date.date()
        elif isoweekday > 5:
            # print 'Its after Friday'
            return (date_time + timedelta(days=(7 - isoweekday) + 5)).date()
        elif isoweekday == 5:
            # print 'Its Friday'
            if type(date_time) == datetime.datetime:
                if date_time.hour >= 14:
                    return self.get_jummah_date(date_time + timedelta(days=1))
                else:
                    return date_time.date()

    def get_this_week_khateeb(self):
        logger.info('Getting this weeks Khateeb')
        return self.get_khateeb_for_date()

    def get_khateeb_for_date(self, d_date=None):
        d_date = d_date if d_date is not None else datetime.datetime.now()
        jummah_date = self.get_jummah_date(d_date)
        logger.info('Getting Khateeb for {} --> {}'.format(d_date, jummah_date))

        result = self.CACHE[self.CACHE['DATE'] == jummah_date]

        if not result.empty:
            khateeb = {'date': self.get_jummah_date(d_date), 'khateeb': result.KHATEEB.values[0]}
            logger.info('Returning: {}'.format(khateeb))

            return khateeb
        else:
            return None

    def _update_cache_thread(self):
        while True:
            logger.info('Updating cache...')
            self.update_cache()
            logger.info('Cache will update again in {} seconds'.format(self.refresh_interval))
            time.sleep(self.refresh_interval)

    def update_cache(self):
        self.CACHE = self.read_data_as_pd(sheet_name=self.SHEET_NAME)
        self.CACHE['DATE'] = self.CACHE['DATE'].apply(string2date)
        logger.info('Cache updated!')

    def run(self):
        try:
            logger.info('Creating update thread cache..')
            cache_thread = threading.Thread(target=self._update_cache_thread,
                                            name='{} Update Thread'.format(self.__class__.__name__))
            cache_thread.setDaemon(True)
            cache_thread.start()
        except KeyboardInterrupt:
            cache_thread.join(1)

    def shutdown(self):
        pass


config = settings.CONFIG.JummahKhateebReader
khateeb_finder = JummahKhateebReader(sheet_id=config['sheet_id'],
                                     client_secret=config['client_secret'],
                                     token_cache=config['token_cache'],
                                     sheet_name=config['sheet_name'],
                                     refresh_interval=config['refresh_interval'])
khateeb_finder.run()
