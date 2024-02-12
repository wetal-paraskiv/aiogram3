import json
import logging

import pytz
import requests
from datetime import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup


class Util:

    def __init__(self):
        pass

    @property
    def logger(self):
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def get_client_date_time_now_from_ip_data(self) -> datetime:
        self.logger.debug("get ip info")
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        ip_data = json.load(response)
        str_client_timezone = ip_data['timezone']
        client_pytz = pytz.timezone(str_client_timezone)
        client_datetime_now = datetime.now(client_pytz)
        return client_datetime_now

    def is_daytime(self) -> bool:
        self.logger.debug("checking time for deactivation during nighttime.")
        client_datetime_now = self.get_client_date_time_now_from_ip_data()

        morning_limit_time = '09:00:00'
        morning_datetime_object = datetime.strptime(morning_limit_time, '%H:%M:%S')
        evening_limit_time = '20:00:00'
        evening_datetime_object = datetime.strptime(evening_limit_time, '%H:%M:%S')

        return morning_datetime_object.time() <= client_datetime_now.time() <= evening_datetime_object.time()

    def get_page_title(self, url) -> str:
        self.logger.debug("retrieving page title")
        source = requests.get(url)
        source.encoding = 'utf-8'
        soup = BeautifulSoup(source.text, 'lxml')
        title_tag = soup.html.head.title
        title = title_tag.get_text().replace('"', '').replace('|', '')
        return title
