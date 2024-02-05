from datetime import datetime
from urllib.request import urlopen
from lxml.html import parse
import json

import pytz


def _get_ip_data() -> dict:
    url = 'http://ipinfo.io/json'
    response = urlopen(url)
    return json.load(response)


def is_daytime() -> bool:
    ip_data = _get_ip_data()
    str_client_timezone = ip_data['timezone']
    client_pytz = pytz.timezone(str_client_timezone)
    client_datetime_now = datetime.now(client_pytz)

    morning_limit_time = '09:00:00'
    morning_datetime_object = datetime.strptime(morning_limit_time, '%H:%M:%S')
    evening_limit_time = '20:00:00'
    evening_datetime_object = datetime.strptime(evening_limit_time, '%H:%M:%S')

    return morning_datetime_object.time() <= client_datetime_now.time() <= evening_datetime_object.time()


def get_page_title(url):
    page = urlopen(url)
    parsed_page = parse(page)
    full_title = parsed_page.find(".//title").text
    title = full_title.replace("|", "")
    return title
