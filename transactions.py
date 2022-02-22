from ScraperModule.SeleniumService.selenium_executor import SeleniumExecutor
from ScraperModule.WaxBloksIo import WaxBloksIo
from ScraperModule.WaxCloud import login_wax_cloud
from TimeModule.TimeModule import TimeModule


class WaxBloksIoTransactions:
    @staticmethod
    def buy(instance, to_name, claimer_name, drop_id, claim_amount, delphi_median, referer, country, buying_time, currency):
        instance.buy_drop(to_name, claimer_name, drop_id, claim_amount, delphi_median, referer, country, buying_time, currency)
        delta_time_1 = 1000
        while TimeModule.return_current_unix_time() + delta_time_1 < buying_time:
            continue
        instance.submit_transaction()
        WaxBloksIoTransactions.try_confirmation(instance)
        status, message = instance.response_message()
        return status, message

    @staticmethod
    def deposit(instance, from_name, to_name, quantity, memo):
        instance.deposit_to_site(from_name, to_name, quantity, memo)
        instance.submit_transaction()
        WaxBloksIoTransactions.try_confirmation(instance)

    @staticmethod
    def get_last_median(instance):
        median, timestamp = instance.check_median()
        return median, timestamp

    @staticmethod
    def get_drop_info(instance, token_id):
        instance.selenium_executor.open_url(instance.driver, 'https://wax.bloks.io/')
        return instance.get_info(token_id)

    @staticmethod
    def try_confirmation(instance):
        try:
            instance.first_transaction()
        except Exception:
            print('Transaction without confirmation window')

