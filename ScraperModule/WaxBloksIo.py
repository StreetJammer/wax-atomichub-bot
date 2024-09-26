import datetime
import time

import pandas as pd

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from DaoModule.Dao import Dao
from TimeModule.TimeModule import TimeModule


class WaxBloksIo:

    def __init__(self, selenium_executor, login_wax_cloud):
        self.login_wax_cloud = login_wax_cloud
        self.selenium_executor = selenium_executor
        self.driver = selenium_executor.get_driver()

    def login_to_waxbloksio(self, wax_login, wax_password):
        # https://wax.bloks.io/ login
        self.selenium_executor.open_url(self.driver, 'https://wax.bloks.io/')

        login_button_xpath = '//*[@id="login-dropdown"]/span'
        self.find_element_and_click(login_button_xpath)
        wax_button_xpath = '//*[@id="header-grid"]/div[3]/div[2]/div/div[2]/div/div[2]/div/div[2]/div'
        wax_button_xpath = "//*[contains(text(),'Cloud Wallet')]"
        self.find_element_and_click(wax_button_xpath)
        handles = self.driver.window_handles
        WebDriverWait(self.driver, 300).until(EC.number_of_windows_to_be(3))
        while len(handles) < 3:
            time.sleep(5)
            handles = self.driver.window_handles
            print(len(handles))
        self.driver.switch_to.window(handles[-1])
        self.login_wax_cloud(self.driver, wax_login, wax_password)
        self.driver.switch_to.window(handles[-1])
        accept_button_xpath = '//*[@id="root"]/div/section/div[2]/div/div[6]/button/div'
        try:
            self.driver.switch_to.window(handles[-1])
            self.find_element_and_click(accept_button_xpath)
        except Exception:
            pass
        self.driver.switch_to.window(handles[0])
        print(self.driver.title)

        return self.driver

    def search_drop(self, name):
        # self.driver.save_screenshot('screen.png')
        search_field_xpath = '//*[@id="search-input-field"]/input'
        search_button_xpath = '//*[@id="search-button"]'
        self.find_element_and_send_key(search_field_xpath, name)
        self.find_element_and_click(search_button_xpath)
        return self.driver

    def _search_lower_upper_bound(self, nft_id):
        input_value = str(nft_id)
        left_bound_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[1]/div[2]/div/div[2]/input'
        right_bound_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[1]/div[2]/div/div[3]/input'
        refresh_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[1]/div[2]/div/div[5]/div'
        self.clear_field(right_bound_xpath)
        self.clear_field(left_bound_xpath)
        self.find_element_and_send_key(left_bound_xpath, input_value)
        self.find_element_and_send_key(right_bound_xpath, input_value)
        self.find_element_and_click(refresh_xpath)

        return self.driver

    def click_contract_tab(self):
        contract_xpath = '//*[@id="top-container"]/div[2]/div[2]'
        self.find_element_and_click(contract_xpath)

    def find_contract_drop(self, nft_id=None):
        self.click_contract_tab()
        drops_xpath = '//*[@id="mobile-buttons"]/div[1]/span[7]'
        self.find_element_and_click(drops_xpath)
        if nft_id:
            self.driver = self._search_lower_upper_bound(nft_id)
        return self.driver

    def parse_listing_price(self):
        listing_price_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[2]/table/tbody/tr/td[5]'
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, listing_price_xpath)))
        td_listing_price = self.driver.find_element(By.XPATH, listing_price_xpath)
        price, currency = td_listing_price.text.split(' ')
        return price, currency

    def find_element_and_click(self, xpath, by=By.XPATH):
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((by, xpath)))
        button = self.driver.find_element(by, xpath)
        # action_chains = ActionChains(self.driver)
        # action_chains.move_to_element(button).perform()
        # action_chains.click().perform()
        try:
            button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", button)
        return self.driver

    def find_element_and_send_key(self, xpath, key, by=By.XPATH):
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((by, xpath)))
        field = self.driver.find_element(by, xpath)
        field.send_keys(key)
        return self.driver

    def clear_field(self, xpath, by=By.XPATH):
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((by, xpath)))
        field = self.driver.find_element(by, xpath)
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        return self.driver

    def buy_drop(self, to_name, claimer_name, drop_id, claim_amount, delphi_median, referer, country, buying_time, currency):
        self.search_drop(to_name)
        self.click_contract_tab()
        # click actions
        self.find_element_and_click('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[3]/div[2]')
        # click claim drop
        old_claimdrop_xpath='//*[@id="top-container"]/div/div[4]/div/div/div/div/div/span[7]'
        claim_drop_xpath = "(//*[contains(text(),'claimdrop')])[1]"
        self.find_element_and_click(claim_drop_xpath)
        # insert claimer [oueyy.wam]
        claimer_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/input'
        self.find_element_and_send_key(claimer_xpath, claimer_name)
        # insert drop_id [1]
        drop_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[2]/div/div/input'
        self.find_element_and_send_key(drop_xpath, drop_id)
        # insert claim_amount [1]
        claim_amount_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[3]/div/div/input'
        self.find_element_and_send_key(claim_amount_xpath, claim_amount)
        # insert referer [atomichub]
        referer_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[5]/div/div/input'
        self.find_element_and_send_key(referer_xpath, referer)
        # insert country [UA]
        country_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[6]/div/div/input'
        self.find_element_and_send_key(country_xpath, country)
        # insert delphi_median [0]
        delphi_median = self.__get_delphi_median(buying_time, currency)
        median_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[4]/div/div/input'
        self.find_element_and_send_key(median_xpath, delphi_median)

    def __get_delphi_median(self, buying_time, currency):
        if currency == 'WAX':
            return 0

        delta_time_5 = 10000
        while TimeModule.return_current_unix_time() + delta_time_5 < buying_time:
            continue
        return Dao.get_median()

        
    def deposit_to_site(self, from_name, to_name, quantity, memo):
        ####  Deposit to site
        self.search_drop('eosio.token')
        self.click_contract_tab()
        # click contract
        self.find_element_and_click('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[3]/div[2]')
        # click actions
        self.find_element_and_click('/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[3]/div[2]')
        # click transfer
        self.find_element_and_click('//*[@id="top-container"]/div/div[4]/div/div/div/div/div/span[6]')
        # insert from [oueyy.wam]
        from_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[1]/div/div/input'
        self.find_element_and_send_key(from_xpath, from_name)
        # insert to [atomicdropsx]
        to_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[2]/div/div/input'
        self.find_element_and_send_key(to_xpath, to_name)
        # insert quantity [1.00000000 WAX]
        quantity_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[3]/div/div/input'
        self.find_element_and_send_key(quantity_xpath, quantity)
        # insert memo [deposit]
        memo_xpath = '//*[@id="top-container"]/div/div[4]/div/div/div/div[2]/div/div[4]/div/div/input'
        self.find_element_and_send_key(memo_xpath, memo)

    def submit_transaction(self):
        submit_button_xpath = '//*[@id="push-transaction-btn"]'
        self.find_element_and_click(submit_button_xpath)

    def first_transaction(self):
        time.sleep(6)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.find_element_and_click('//*[@id="root"]/div/section/div[2]/div/div[4]/label/span[1]/span[1]/input')
        self.find_element_and_click('//*[@id="root"]/div/section/div[2]/div/div[5]/button/div')
        self.driver.switch_to.window(handles[0])

    def response_message(self):
        message_xpath = "//*[contains(concat(' ', @class, ' '), 'message')]"
        message_status_xpath = "//*[contains(concat(' ', @class, ' '), 'message')]/div"
        message_text_xpath = "//*[contains(concat(' ', @class, ' '), 'message')]/p"
        message = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, message_xpath)))
        message_status = self.driver.find_element(By.XPATH, message_status_xpath).text
        message_text = self.driver.find_element(By.XPATH, message_text_xpath).text
        return message_status, message_text

    def get_claimer_name(self):
        name_xpath = '//*[@class="desktop-account-header header"]/div/div'
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, name_xpath)))
        name = self.driver.find_element(By.XPATH, name_xpath).text
        return name.split(" ")[0]

    def get_table(self, xpath, by=By.XPATH):
        WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((by, xpath)))
        html_table = self.driver.find_element(by, xpath)
        df = pd.read_html(html_table.get_attribute('outerHTML'))[0]
        # print(df.head())
        return df

    def get_listing_price(self, nft_id, to_name):
        self.search_drop(to_name)
        self.find_contract_drop(nft_id=nft_id)
        table_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[2]/table'
        df = self.get_table(table_xpath)
        listing_price = df.loc[0, 'listing_price']
        return listing_price

    def get_info(self, nft_id, to_name):
        self.search_drop(to_name)
        self.find_contract_drop(nft_id=nft_id)
        time.sleep(3)
        table_xpath = "/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[2]/table"
        df = self.get_table(table_xpath)
        info_dict = {
            "drop_id": int(df.loc[0, 'drop_id (key)']),
            "collection_name": str(df.loc[0, 'collection_name']),
            "price": float(df.loc[0, 'listing_price'].split(" ")[0]),
            "currency": str(df.loc[0, 'listing_price'].split(" ")[1]),
            "settlement_symbol": str(df.loc[0, 'settlement_symbol']),
            "price_recipient": str(df.loc[0, 'price_recipient']),
            "fee_rate": float(df.loc[0, 'fee_rate']),
            "auth_required": int(df.loc[0, 'auth_required']),
            "account_limit": int(df.loc[0, 'account_limit']),
            "account_limit_cooldown": int(df.loc[0, 'account_limit_cooldown']),
            "max_claimable": int(df.loc[0, 'max_claimable']),
            "current_claimed": int(df.loc[0, 'current_claimed']),
            "start_time": int(df.loc[0, 'start_time']), #self._return_datetime_format_from_obj(df.loc[0, 'start_time']),
            "end_time": int(df.loc[0, 'end_time']), #self._return_datetime_format_from_obj(df.loc[0, 'end_time']),
            "scraped_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        return info_dict
    
    def check_median(self):
        ### Check median
        scope = 'waxpusd'
        self.search_drop('delphioracle')
        self.click_contract_tab()

        # click datapoints
        self.find_element_and_click('//*[@id="mobile-buttons"]/div[1]/span[4]')

        # clear Scope
        scope_xpath = '//*[@id="mobile-buttons"]/div[2]/div/div[1]/input'
        self.clear_field(scope_xpath)
        # insert Scope
        self.find_element_and_send_key(scope_xpath, scope)

        # click refresh button
        refresh_xpath = '//*[@id="mobile-buttons"]/div[2]/div/div[5]/div'
        self.find_element_and_click(refresh_xpath)

        table_xpath = '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[4]/div/div/div[2]/table'
        df = self.get_table(table_xpath)
        df.sort_values(['timestamp'])
        median = df.loc[0, 'median']
        timestamp = df.loc[0, 'timestamp']
        return median, timestamp


    def _return_datetime_format_from_obj(self, obj):
        try:
            string = str(obj).replace("T", " ")
            return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S.%f').isoformat()
        except Exception:
            return ''
