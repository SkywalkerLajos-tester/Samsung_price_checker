import pytest
import allure
import time
import os
import datetime
import csv

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

    def teardown_method(self):
        self.main_page.close_browser()


    def mentes_csv_fajlba(self, eredeti_ar, akcios_ar, torzsvasarloi_ar):
        CSV_FILE = "POM_SES_price_check/S26_Ultra_POM_arak.csv"
        """
        Az árakat egy csv fájlba menti. Ha a mai napra már létezik sor,
        azt felülírja a friss adatokkal, így naponta csak egyszer szerepel
        egy adott dátum a fájlban, függetlenül attól, hányszor futtatjuk.
        """
        ma = datetime.date.today().strftime("%Y.%m.%d.")
        fejlec = ["Lekérdezés napja", "Eredeti ár (Ft)", "Akciós ár (Ft)", "Törzsvásárlói ár (Ft)"]

        adat_sorok = []
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, "r", newline="", encoding="utf-8") as fajl:
                reader = csv.reader(fajl)
                sorok = list(reader)
            if sorok and sorok[0] == fejlec:
                adat_sorok = sorok[1:]
            else:
                adat_sorok = sorok

        # Eltávolítjuk a mai naphoz tartozó korábbi sort, ha van
        adat_sorok = [sor for sor in adat_sorok if sor and sor[0] != ma]

        # Hozzáadjuk a friss, mai napi sort
        adat_sorok.append([ma, eredeti_ar, akcios_ar, torzsvasarloi_ar])

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as fajl:
            writer = csv.writer(fajl)
            writer.writerow(fejlec)
            writer.writerows(adat_sorok)

        teljes_utvonal = os.path.abspath(CSV_FILE)
        print(f"\n Az árak elmentve a csv fájlba: {teljes_utvonal}")
        assert os.path.exists(CSV_FILE), f"A csv fájl mentése nem sikerült ide: {teljes_utvonal}"


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
        time.sleep(0.5)
        self.logged_in_page.color().click()
        self.logged_in_page.size().click()

        self.browser.execute_script("window.scrollBy(0, 205);")

        self.selection_result_page.selected_item().click()

        self.browser.execute_script("window.scrollBy(0, 240);")

        eredeti_ar = self.S26Ultra_item_page.eredeti_ar()
        print(f'\n Eredeti ár: {eredeti_ar.text}')
        levagott_eredeti_ar = int(eredeti_ar.text.replace(" ", "").replace("Ft", "").strip())
        print(levagott_eredeti_ar)

        akcios_ar = self.S26Ultra_item_page.akcios_ar()
        akcios_ar_csak = akcios_ar.text.replace(eredeti_ar.text, "").strip()
        print(f'\n Akciós ár: {akcios_ar_csak}')
        levagott_akcios_ar = int(akcios_ar_csak.replace(" ", "").replace("Ft", "").strip())
        print(levagott_akcios_ar)

        torzsvasarloi_ar = self.S26Ultra_item_page.torzsvasarloi_ar()
        print(f'\n Törzsvásárlói ár: {torzsvasarloi_ar.text}')
        levagott_torzsvasarloi_ar = int(torzsvasarloi_ar.text.replace(" ", "").replace("Ft", "").strip())
        print(levagott_torzsvasarloi_ar)

        akcio_merteke_szazalekban = (round(1 - (levagott_akcios_ar / levagott_eredeti_ar), 4)) * 100
        akcio_merteke_forintban = levagott_eredeti_ar - levagott_akcios_ar
        print(f'\n Az akció mértéke: {akcio_merteke_szazalekban}%, ami {akcio_merteke_forintban} forintnak felel meg')

        teljes_kedvezmeny_szazalekben = (round(1 - (levagott_torzsvasarloi_ar / levagott_eredeti_ar), 4)) * 100
        teljes_kedvezmeny_forintban = levagott_eredeti_ar - levagott_torzsvasarloi_ar
        print(
            f'\n A teljes kedvezmény mértéke: {teljes_kedvezmeny_szazalekben}%, ami {teljes_kedvezmeny_forintban} forintnak felel meg')
        print(
            f'\n Mindez azt jelenti hogy {eredeti_ar.text} helyett most minden kezdvezményt figyelembe véve {torzsvasarloi_ar.text}-be kerül egy 512 Mb-os feketes S26 Ultra készülék.')

        self.mentes_csv_fajlba(levagott_eredeti_ar, levagott_akcios_ar, levagott_torzsvasarloi_ar)
