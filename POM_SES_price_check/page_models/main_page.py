from POM_SES_price_check.general_page import GeneralPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class SES(GeneralPage):
    def __init__(self, browser, URL):
        super().__init__(browser, URL)
        self.wait = WebDriverWait(self.browser, 5)


    def accept_cookies(self):
        return self.wait.until(EC.element_to_be_clickable((By.ID, "cc-accept-all")))

    def login(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[normalize-space()='Fiók'])[1]")))





