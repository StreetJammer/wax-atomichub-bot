import time

import pandas as pd
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from ScraperModule.WaxCloud import login_wax_cloud
from ScraperModule.SeleniumService.selenium_executor import SeleniumExecutor


class AtomicHub:
    def __init__(self, selenium_executor, login_wax_cloud):
        self.selenium_executor = selenium_executor
        self.driver = selenium_executor.get_driver()
        self.login_wax_cloud = login_wax_cloud

    def login_to_atomichub(self, wax_login, wax_password):
        # https://wax.atomichub.io/ login
        selenium_executor = SeleniumExecutor()
        selenium_executor.open_url(self.driver, 'https://wax.atomichub.io/')
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div/div/div/div[2]/button[1]')))
        accept_cookie_button = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/button[1]')
        accept_cookie_button.click()
        WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="root"]/nav/div/div[4]/div/button')))
        login_button = self.driver.find_element(By.XPATH, '//*[@id="root"]/nav/div/div[4]/div/button')
        login_button.click()
        WebDriverWait(self.driver, 20).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/button')))
        wax_button = self.driver.find_element(By.XPATH,
                                              '/html/body/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/button')
        wax_button.click()
        time.sleep(15)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.login_wax_cloud(self.driver, wax_login, wax_password)
        self.driver.switch_to.window(handles[0])
        print(self.driver.title)

        return self.driver

    def get_token_info(self, drop_id):
        self.selenium_executor.open_url(self.driver, f'https://wax.atomichub.io/drops/{drop_id}')
        table_xpath = '//*[@id="root"]/div[2]/div/div[2]/div/div/div/div[1]/div[3]/div/table'
        WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located(
            (By.XPATH, table_xpath)))
        html_table = self.driver.find_element(By.XPATH, table_xpath)
        df = pd.read_html(html_table.get_attribute('outerHTML'))[0]
        info_dict = {}
        info_dict["Name"] = df[1][0].replace('#', '')
        info_dict["Seller"] = df[1][1]
        info_dict[df[0][3]] = df[1][3]
        return info_dict

    @staticmethod
    def get_token_api_info(drop_id):
        response = requests.get("https://wax.api.atomicassets.io/atomicassets/v1/templates/farmersworld/260616")
        return response.json()
