from POM_SES_price_check.general_page import GeneralPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class LoginPage(GeneralPage):
    def __init__(self, browser, URL):
        super().__init__(browser, URL)
        self.wait = WebDriverWait(self.browser, 5)

    def email_address(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='email'])[1]")))

    def enter_password(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@type='password'])[1]")))

    def button_sign_in(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

