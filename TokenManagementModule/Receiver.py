from datetime import datetime, timedelta
from typing import List

import pytz

from DaoModule.Dao import Dao
from ScraperModule.SeleniumService.selenium_executor import SeleniumExecutor
from ScraperModule.WaxBloksIo import WaxBloksIo
from ScraperModule.WaxCloud import login_wax_cloud
from transactions import WaxBloksIoTransactions



class Receiver:
    def __init__(self, dao=None, db_url=None):
        self.db_url = db_url
        self.dao = dao
        self.transactions = WaxBloksIoTransactions()

    def receive_data(self, login_data: List[dict], token_ids: List[int], buy_nft, to_name):
        selenium_executor = SeleniumExecutor()
        req = WaxBloksIo(selenium_executor, login_wax_cloud)
        req.selenium_executor.open_url(req.driver, 'https://wax.bloks.io/')
        for token in token_ids:
            token_info = req.get_info(token, to_name)
            token_id = self.save_token_to_db(token_info)
            for credentials in login_data:
                account_id = self.save_credentials_to_db(credentials)
                task_id = self.save_task_to_db(token_id=token_id, account_id=account_id)
                self.send_to_celery(token_info, credentials, task_id, buy_nft, to_name)
        req.driver.close()

    def scrape_token_info(self, token, to_name):
        selenium_executor = SeleniumExecutor()
        req = WaxBloksIo(selenium_executor, login_wax_cloud)
        req.selenium_executor.open_url(req.driver, 'https://wax.bloks.io/')
        token_info = req.get_info(token, to_name)
        self.save_token_to_db(token_info)
        req.driver.close()

    def send_to_celery(self, token_info, credentials, task_id, buy_nft, to_name):
        time_diff = 60  #seconds
        eta = datetime.utcfromtimestamp(token_info['start_time'] - time_diff)
        buy_nft.apply_async(eta=eta,  #datetime.now(pytz.utc) + timedelta(seconds=15),
                            kwargs={
                                "token": token_info,
                                "credentials": credentials,
                                "task_id": task_id,
                                "to_name": to_name,
                                    })

    def save_task_to_db(self,
                        token_id,
                        account_id,
                        added_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        perform_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        status='In Progress',
                        error='',
                        ):
        return Dao.add_task(account_id, token_id, added_time, perform_time, status, error)

    def save_credentials_to_db(self, credentials):
        return Dao.add_account(
            login=credentials["login"],
            password=credentials["password"]
        )

    def save_token_to_db(self, token_info):
        print(token_info)
        return Dao.add_token(
            drop_id=token_info['drop_id'],
            collection_name=token_info['collection_name'],
            price=token_info['price'],
            currency=token_info['currency'],
            settlement_symbol=token_info['settlement_symbol'],
            price_recipient=token_info['price_recipient'],
            fee_rate=token_info['fee_rate'],
            auth_required=token_info['auth_required'],
            account_limit=token_info['account_limit'],
            account_limit_cooldown=token_info['account_limit_cooldown'],
            max_claimable=token_info['max_claimable'],
            current_claimed=token_info['current_claimed'],
            start_time=token_info['start_time'], # or datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            end_time=token_info['end_time'], # or datetime(year=3000, month=12, day=12).strftime('%Y-%m-%d %H:%M:%S')
        )

