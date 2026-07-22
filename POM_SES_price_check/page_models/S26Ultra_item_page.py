from POM_SES_price_check.general_page import GeneralPage
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select


class S26Ultra(GeneralPage):
    def __init__(self, browser, URL):
        super().__init__(browser, URL)
        self.wait = WebDriverWait(self.browser, 5)

    def eredeti_ar(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='text-gray-400 line-through text-lg mr-3']")))

    def akcios_ar(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='text-[32px] font-bold mb-4 tracking-tight']")))

    def torzsvasarloi_ar(self):
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mt-1 text-3xl font-bold text-emerald-700']")))