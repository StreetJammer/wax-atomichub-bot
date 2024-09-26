import os
from datetime import datetime
from dateutil.parser import parse

import requests
from dotenv import load_dotenv

load_dotenv()
flask_url = os.getenv('FLASK_HOST')

class Dao:

    @staticmethod
    def get_median():
        response = requests.get(flask_url+"median/", timeout=10)
        response_json = response.json()
        median = response_json['result'][0]['price']
        return median

    @staticmethod
    def get_tokens():
        response = requests.get(flask_url + "tokens/", timeout=10)
        response_json = response.json()
        return response_json['result']

    @staticmethod
    def add_account(login, password):
        r = requests.post(flask_url + 'add-account/', json={
            "login": login,
            "password": password,
        }, timeout=10)
        return r.json()['account']

    @staticmethod
    def add_task(account_id, token_id, added_time, perform_time, status, error):
        r = requests.post(flask_url + 'add-task/', json={
            "account_id": account_id,
            "token_id": token_id,
            "added_time": added_time,
            "perform_time": perform_time,
            "status": status,
            "error": error,
        }, timeout=10)
        return r.json()['task']

    @staticmethod
    def update_task(task_id, perform_time, status, error):
        r = requests.put(flask_url + 'update-task/', json={
            "task_id": task_id,
            "perform_time": perform_time,
            "status": status,
            "error": error,
        }, timeout=10)
        })
        return r.json()["success"]

    @staticmethod
    def add_token(drop_id, collection_name, price, currency, settlement_symbol, price_recipient,
                  fee_rate, auth_required, account_limit, account_limit_cooldown, max_claimable,
                  current_claimed, start_time, end_time):
        r = requests.post(flask_url + 'add-token/', json={
            "drop_id": drop_id,
            "collection_name": collection_name,
            "price": price,
            "currency": currency,
            "settlement_symbol": settlement_symbol,
            "price_recipient": price_recipient,
            "fee_rate": fee_rate,
            "auth_required": auth_required,
            "account_limit": account_limit,
            "account_limit_cooldown": account_limit_cooldown,
            "max_claimable": max_claimable,
            "current_claimed": current_claimed,
            "start_time": datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S'),
            "end_time": datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S'),
            "scraped_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        })
        return r.json()["token"]

    @staticmethod
    def get_history_data(token_id, number_of_days):
        r = requests.post(flask_url + 'plot-data/', json={
            "token_id": token_id,
            "number_of_days": number_of_days
        })
        print(f"Status Code: {r.status_code}, Response: {r}")
        return r.json()["result"][::-1]

    @staticmethod
    def get_clean_historical_data(drop_id, number_of_days=30):
        data = Dao.get_history_data(drop_id, number_of_days)
        print(data)
        labels = []
        values = []
        for elem in data:
            labels.append(parse(elem['add_time']).strftime('%m-%d-%Y'))
            values.append(elem['price'])
        return labels, values

    @staticmethod
    def get_drop_ids():
        r = requests.get(flask_url + '/get-nft-ids/')
        token_ids = []
        for token in r.json()['result']:
            token_ids.append(token['drop_id'])
        return token_ids



if __name__ == '__main__':
    # print(Dao.add_token(
    #     drop_id=111,
    #     collection_name='TEST',
    #     price=112.2,
    #     currency='WAX',
    #     settlement_symbol='wax',
    #     price_recipient='myself',
    #     fee_rate=0.222,
    #     auth_required=0,
    #     account_limit=1,
    #     account_limit_cooldown=2,
    #     max_claimable=100,
    #     current_claimed=10,
    #     start_time=None,
    #     end_time='2021-12-03 17:12:00.500000'
    # ))
    print(Dao.get_history_data(1, 30))
