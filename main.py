import time

from ScraperModule.AtomicHub import AtomicHub
from ScraperModule.SeleniumService.selenium_executor import SeleniumExecutor
from ScraperModule.WaxBloksIo import WaxBloksIo
from ScraperModule.WaxCloud import login_wax_cloud
from TimeModule.TimeModule import TimeModule
from transactions import WaxBloksIoTransactions

CONSTS = {
    'wax_cloud_login': 'mykola.kurenkov@data-ox.com',
    'wax_cloud_password': 'TestTest123$',
    'claimer_name': 'oueyy.wam',
    'drop_id': 1,
    'claim_amount': 1,
    'delphi_median': 0,
    'referer': 'atomichub',
    'country': 'UA',
    'from': 'oueyy.wam',
    'to': 'atomicdropsx',
    'quantity': '1.00000000 WAX',
    'memo': 'deposit'
}


def buy_check(login, password, drop_id, to_name, referer, country, buying_time, delphi_median=0, claim_amount=1, currency='WAX'):
    selenium_executor = SeleniumExecutor()
    req = WaxBloksIo(selenium_executor, login_wax_cloud)
    req.login_to_waxbloksio(wax_login=login, wax_password=password)
    claimer_name = req.get_claimer_name()
    transactions = WaxBloksIoTransactions()

    response = transactions.buy(req, to_name, claimer_name, drop_id, claim_amount, delphi_median, referer, country, buying_time, currency)
    req.driver.close()
    return response

def deposit():
    claimer_name = CONSTS['claimer_name']
    drop_id = CONSTS['drop_id']
    claim_amount = CONSTS['claim_amount']
    delphi_median = CONSTS['delphi_median']
    referer = CONSTS['referer']
    country = CONSTS['country']
    ### Deposit drop
    from_name = CONSTS['from']
    to_name = CONSTS['to']
    quantity = CONSTS['quantity']
    memo = CONSTS['memo']


    selenium_executor = SeleniumExecutor()
    req = WaxBloksIo(selenium_executor, login_wax_cloud)
    req.login_to_waxbloksio(wax_login=CONSTS['wax_cloud_login'], wax_password=CONSTS['wax_cloud_password'])
    token_id_1 = 85968
    transactions = WaxBloksIoTransactions()
    transactions.deposit(req, from_name, to_name, quantity, memo)

def get_drop_info():
    selenium_executor = SeleniumExecutor()
    req = WaxBloksIo(selenium_executor, login_wax_cloud)
    #req.login_to_atomichub(wax_login=CONSTS['wax_cloud_login'], wax_password=CONSTS['wax_cloud_password'])
    token_id_1 = 85968
    token_id_2 = 86011
    transactions = WaxBloksIoTransactions()
    token_info = transactions.get_drop_info(req, token_id_2)
    print(token_info)



if __name__ == '__main__':
    deposit()



    #buy_check()

    # WaxBloksIoTransactions.deposit(req, from_name, to_name, quantity, memo)
    # WaxBloksIoTransactions.buy(req, claimer_name, drop_id, claim_amount, delphi_median, referer, country)
    # selenium_executor.close_drivers()









