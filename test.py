import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.parser import parse

import pytz

from DaoModule.Dao import Dao
from TokenManagementModule.Receiver import Receiver
from BuyingModule.celery_task import buy_nft
load_dotenv()
broker = os.getenv('BROKER')

# receiver = Receiver()
# receiver.receive_data([{"login": "mykola.kurenkov@data-ox.com", "password": "TestTest123$"}], [1,])

# data = Dao.get_history_data(1, 30)
# print(data)
# labels = []
# values = []
# for elem in data:
#
#     labels.append(parse(elem['add_time']).strftime('%m-%d-%Y'))
#     values.append(elem['price'])
#
# print(labels)
# print(values)

# receiver = Receiver()
# receiver.receive_data([{"login": "mykola.kurenkov@data-ox.com", "password": "TestTest123$"}], [1,], buy_nft)

import pytest

@pytest.fixture
def setup():
    # Setup code if necessary
    pass

def test_buy_transaction():
    # Implement test for WaxBloksIoTransactions.buy
    assert True  # Replace with actual assertions

def test_deposit_transaction():
    # Implement test for WaxBloksIoTransactions.deposit
    assert True  # Replace with actual assertions