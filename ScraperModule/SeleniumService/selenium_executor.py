import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumExecutor:
    def __init__(self):
        self.drivers = []

    def get_driver(self):
        # options = Options()
        # #options.add_argument("--headless")
        # options.add_argument("window-size=1400,600")
        # options.add_experimental_option("detach", True)
        # path = os.getcwd()
        # driver = webdriver.Chrome(path + '/ScraperModule/SeleniumService/driver/chromedriver', chrome_options=options)
        op = webdriver.ChromeOptions()
        op.add_argument("--window-size=1920,1080")
        op.add_argument('--no-sandbox')
        op.add_argument('--headless')
        op.add_argument('--disable-dev-shm-usage')
        op.add_argument('--ignore-certificate-errors')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        op.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
        path = os.getcwd()
        #driver = webdriver.Chrome(path + '/ScraperModule/SeleniumService/driver/chromedriver', chrome_options=op)
        self.drivers.append(driver)
        return driver

    @staticmethod
    def open_url(driver, url):
        driver.get(url)
        return driver

    def close_drivers(self):
        for driver in self.drivers:
            driver.close()
