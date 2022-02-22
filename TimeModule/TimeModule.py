import os
import re, time
from datetime import datetime

import pytz
import requests
from dotenv import load_dotenv

load_dotenv()
url = os.getenv('TIME_URL')


class TimeModule:
    @staticmethod
    def return_current_date_time():
        response = requests.get(url)
        str_response = str(response.content)
        unix_time = re.search(r'\d+', str_response).group()
        unix_time_float = float(unix_time) / 1000.0
        date_time = datetime.utcfromtimestamp(unix_time_float).strftime('%Y-%m-%d %H:%M:%S.%f')
        return date_time

    @staticmethod
    def return_current_unix_time():
        response = requests.get(url)
        str_response = str(response.content)
        unix_time = re.search(r'\d+', str_response).group()
        return float(unix_time)


if __name__ == '__main__':
    # LIMIT_TIME = time.time() * 1000 + 5000
    #
    # while TimeModule.return_current_unix_time() < LIMIT_TIME:
    #     continue
    # print(time.time() * 1000)
    # print(TimeModule.return_current_unix_time() - 1000)
    # print(1597759200 * 1000)
    print(datetime.utcfromtimestamp(1597770000).strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.utcfromtimestamp(1597770000 - 60))
