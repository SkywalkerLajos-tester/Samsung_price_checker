import pytest
import allure
import json
import time

from POM_SES_price_check.general_page import GeneralPage
from POM_SES_price_check.page_models.main_page import SES
from POM_SES_price_check.page_models.login_page import LoginPage
from POM_SES_price_check.page_models.logged_in_page import LoggedIn
from POM_SES_price_check.page_models.selection_result_page import SelectedItem
from POM_SES_price_check.page_models.S26Ultra_item_page import S26Ultra
from POM_SES_price_check.create_driver import get_configured_chrome_driver

URL = "https://ses.hu/"


class TestPriceCheck:
    def setup_method(self):
        self.browser = get_configured_chrome_driver()
        self.general_page = GeneralPage(self.browser, URL)
        self.main_page = SES(self.browser, URL)
        self.login_page = LoginPage(self.browser, URL)
        self.logged_in_page = LoggedIn(self.browser, URL)
        self.selection_result_page = SelectedItem(self.browser, URL)
        self.S26Ultra_item_page = S26Ultra(self.browser, URL)

    # def teardown_method(self):
    #     self.main_page.close_browser()


    def test_S26Ultra_price_check(self):
        self.general_page.open_webpage()
        self.main_page.accept_cookies().click()
        self.main_page.login().click()
        time.sleep(1)

        self.login_page.email_address().send_keys("gagman@freemail.hu")
        self.login_page.enter_password().send_keys("Test1234")

        button = self.login_page.button_sign_in()
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        time.sleep(0.5)
        button.click()

        current_user = self.logged_in_page.button_user().text
        assert current_user == "Szabó Zoltán"

        self.logged_in_page.mobil().click()
        self.logged_in_page.galaxy_s().click()
        self.logged_in_page.s26_ultra().click()
        self.logged_in_page.color().click()
        self.logged_in_page.size().click()

        self.browser.execute_script("window.scrollBy(0, 205);")

        self.selection_result_page.selected_item().click()

        self.browser.execute_script("window.scrollBy(0, 240);")
