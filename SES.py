import pytest
import time
import os
import datetime
import csv
###########################################################################

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver import Keys, ActionChains


URL = "https://ses.hu/" #########   BEMÁSOLNI   ###########

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arak.csv")  ###########   ITT ÁLLÍTHATÓ A CSV FÁJL NEVE / ÚTVONALA   ###########

class TestPriceCheckSES: ###########################   ÁTÍRNI   ##########################################

    def setup_method(self):
        options = Options()
        options.add_experimental_option('detach', True)
        options.add_argument('--guest')
        options.add_argument("--lang=hu")  # hu (magyar) vagy en (angol), böngésző nyelve
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        self.browser.get(URL)

    ################################   VISSZATENNI A VÉGÉN  ###################################################
    def teardown_method(self):
        self.browser.close()
    ################################   VISSZATENNI A VÉGÉN  ###################################################

    def test_TC01(self):
        accept_cookies = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, "cc-accept-all")))
        accept_cookies.click()

        login = self.browser.find_element(By.XPATH, "(//span[normalize-space()='Fiók'])[1]")
        login.click()

        email = self.browser.find_element(By.XPATH, "(//input[@type='email'])[1]")
        email.send_keys("gagman@freemail.hu")

        password = self.browser.find_element(By.XPATH, "(//input[@type='password'])[1]")
        password.send_keys("Test1234")

        submit = self.browser.find_element(By.XPATH, "//button[@type='submit']")
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit)
        time.sleep(0.5)
        submit.click()
        time.sleep(0.5)

        mobil = self.browser.find_element(By.XPATH, "(//button[normalize-space()='Mobil'])[1]")
        mobil.click()

        galaxy_s = self.browser.find_element(By.XPATH, "(//span[normalize-space()='Galaxy S széria'])[1]")
        galaxy_s.click()

        s26_ultra = self.browser.find_element(By.XPATH, "//label[text()='Galaxy S26 Ultra']/../input")
        s26_ultra.click()

        color = self.browser.find_element(By.XPATH, "//span/span[text()='Fekete és árnyalatai']/../../input")
        self.browser.execute_script("arguments[0].click();", color)

        size = self.browser.find_element(By.XPATH, "//label/span[text()='512 GB']/../input")
        size.click()

        self.browser.execute_script("window.scrollBy(0, 205);")

        datasheet = self.browser.find_element(By.XPATH, "(//a[@href='/product/samsung-sm-s948ds-black-s26-ultra-dual-esim-512gb'])[1]")
        datasheet.click()

        self.browser.execute_script("window.scrollBy(0, 230);")

        eredeti_ar = self.browser.find_element(By.XPATH, "//span[@class='text-gray-400 line-through text-lg mr-3']")
        print(f'\n Eredeti ár: {eredeti_ar.text}')
        levagott_eredeti_ar = int(eredeti_ar.text.replace(" ", "").replace("Ft", "").strip())
        print(levagott_eredeti_ar)

        akcios_ar = self.browser.find_element(By.XPATH, "//div[@class='text-[32px] font-bold mb-4 tracking-tight']")
        akcios_ar_csak = akcios_ar.text.replace(eredeti_ar.text, "").strip()
        print(f'\n Akciós ár: {akcios_ar_csak}')
        levagott_akcios_ar = int(akcios_ar_csak.replace(" ", "").replace("Ft", "").strip())
        print(levagott_akcios_ar)

        torzsvasarloi_ar = self.browser.find_element(By.XPATH, "//div[@class='mt-1 text-3xl font-bold text-emerald-700']")
        print(f'\n Törzsvásárlói ár: {torzsvasarloi_ar.text}')
        levagott_torzsvasarloi_ar = int(torzsvasarloi_ar.text.replace(" ", "").replace("Ft", "").strip())
        print(levagott_torzsvasarloi_ar)

        akcio_merteke_szazalekban = (round(1-(levagott_akcios_ar/levagott_eredeti_ar), 4))*100
        akcio_merteke_forintban = levagott_eredeti_ar - levagott_akcios_ar
        print(f'\n Az akció mértéke: {akcio_merteke_szazalekban}%, ami {akcio_merteke_forintban} forintnak felel meg')

        teljes_kedvezmeny_szazalekben = (round(1-(levagott_torzsvasarloi_ar/levagott_eredeti_ar), 4))*100
        teljes_kedvezmeny_forintban = levagott_eredeti_ar - levagott_torzsvasarloi_ar
        print(f'\n A teljes kedvezmény mértéke: {teljes_kedvezmeny_szazalekben}%, ami {teljes_kedvezmeny_forintban} forintnak felel meg')
        print(f'\n Mindez azt jelenti hogy {eredeti_ar.text} helyett most minden kezdvezményt figyelembe véve {torzsvasarloi_ar.text}-be kerül egy 512 Mb-os feketes S26 Ultra készülék.')

        self.mentes_csv_fajlba(levagott_eredeti_ar, levagott_akcios_ar, levagott_torzsvasarloi_ar)


    def mentes_csv_fajlba(self, eredeti_ar, akcios_ar, torzsvasarloi_ar):
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
