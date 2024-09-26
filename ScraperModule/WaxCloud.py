
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def login_wax_cloud(driver, wax_login, wax_password):
    # https://wallet.wax.io/ login
    print(driver.title)
    try:
        username_xpath = "//input[@name='userName']"
        password_xpath = "//input[@name='password']"
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, username_xpath)))
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, password_xpath)))
    except SpecificException:
        driver.refresh()
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.NAME, 'userName')))
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.NAME, 'password')))
    while True:
        try:
            username = driver.find_element(By.NAME, 'userName')
            password = driver.find_element(By.NAME, 'password')
            username.send_keys(wax_login)
            password.send_keys(wax_password)
        except SpecificException:
            continue
        break
    submit = driver.find_element(By.CSS_SELECTOR, ".button-primary")
    submit.click()
