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

    def _get_ip_data(self) -> dict:
        self.logger.debug("get ip info")
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        return json.load(response)

    def is_daytime(self) -> bool:
        self.logger.debug("checking time for deactivation during nighttime.")
        ip_data = self._get_ip_data()
        str_client_timezone = ip_data['timezone']
        client_pytz = pytz.timezone(str_client_timezone)
        client_datetime_now = datetime.now(client_pytz)

        morning_limit_time = '09:00:00'
        morning_datetime_object = datetime.strptime(morning_limit_time, '%H:%M:%S')
        evening_limit_time = '20:00:00'
        evening_datetime_object = datetime.strptime(evening_limit_time, '%H:%M:%S')

        return morning_datetime_object.time() <= client_datetime_now.time() <= evening_datetime_object.time()

    def get_page_title(self, url):
        self.logger.debug("retrieving page title")
        source = requests.get(url)
        source.encoding = 'utf-8'
        soup = BeautifulSoup(source.text, 'lxml')
        title_tag = soup.html.head.title
        title = title_tag.get_text().replace('"', '').replace('|', '')
        return title

    def get_data(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        head = soup.html.head
        print(head)
        return
