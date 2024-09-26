import os
from datetime import datetime

import pytz
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

from DaoModule.Dao import Dao
from EmailModule.sender import EmailSender
from TokenManagementModule.Receiver import Receiver
from main import buy_check

load_dotenv()
broker = os.getenv('BROKER_URL')

app = Celery(
    'simple_worker',
    broker=broker,
    backend='db+sqlite:///results.db'
)


@app.task(name='check_nft_data')
def check_nft_data():
    token_ids = Dao.get_drop_ids()
    for token in token_ids:
        scrap_token.apply_async(eta=datetime.now(pytz.utc),
                                kwargs={
                                    "token": token,
                                })
    return True


app.conf.beat_schedule = {
    'checking_the_nft_data': {
        'task': 'check_nft_data',
        'schedule': crontab(minute=30, hour=0),
        # 'args': (16, 16)
    },
}
app.conf.timezone = 'UTC'


@app.task
def scrap_token(**kwargs):
    try:
        token = kwargs['token']
        receiver = Receiver()
        receiver.scrape_token_info(token)
    except SpecificException as err:  # Replace SpecificException with the appropriate exception
        EmailSender(err, 'Error', 'mykola.kurenkov@data-ox.com')


@app.task
def buy_nft(**kwargs):
    try:
        token = kwargs['token']
        credentials = kwargs['credentials']
        task_id = kwargs['task_id']
        to_name = kwargs['to_name']
        print(token)
        print(credentials)
        print(task_id)
        response_status, response_message = buy_check(
            login=credentials['login'],
            password=credentials['password'],
            drop_id=token['drop_id'],
            to_name=to_name,
            referer='atomichub',
            country='US',
            delphi_median=0,
            buying_time=token['start_time'],
            currency=token['currency']
        )
        print(response_status)
        print(response_message)
        EmailSender(response_message,
                    f'Drop #{token["drop_id"]}: {response_status}, {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
                    'mykola.kurenkov@data-ox.com'
                    )
        if response_status == 'Error':
            Dao.update_task(task_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Error', response_message)
        else:
            Dao.update_task(task_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Success', "")
    except SpecificException as err:  # Replace SpecificException with the appropriate exception
        EmailSender(err, 'Error', 'mykola.kurenkov@data-ox.com')


@app.task
def receive_task(**kwargs):
    try:
        login = kwargs['login']
        password = kwargs['password']
        drops = kwargs['drops']
        to_name = kwargs['to_name']
        receiver = Receiver()
        receiver.receive_data([{"login": login, "password": password}], drops, buy_nft, to_name)
    except SpecificException as err:  # Replace SpecificException with the appropriate exception
        print(err)
        login = kwargs['login']
        password = kwargs['password']
        drops = kwargs['drops']
        to_name = kwargs['to_name']
        receiver = Receiver()
        receiver.receive_data([{"login": login, "password": password}], drops, buy_nft, to_name)
    except Exception as err:
        print(err)
