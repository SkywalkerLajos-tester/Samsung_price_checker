
from POM_SES_price_check.general_page import GeneralPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class LoggedIn(GeneralPage):
    def __init__(self, browser, URL):
        super().__init__(browser, URL)
        self.wait = WebDriverWait(self.browser, 10)

    def button_user(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='max-w-[160px] truncate']")))

    def mobil(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Mobil'])[1]")))

    def galaxy_s(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[normalize-space()='Galaxy S széria'])[1]")))

    def s26_ultra(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[text()='Galaxy S26 Ultra']/../input")))

    def color(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span/span[text()='Fekete és árnyalatai']/../../input")))

    def size(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label/span[text()='512 GB']/../input")))