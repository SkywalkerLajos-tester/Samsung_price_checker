import time


class GeneralPage:
    def __init__(self, browser, url):
        self.browser = browser
        self.url = url

    def open_webpage(self):
        self.browser.get(self.url)

    def close_browser(self):
        self.browser.close()

    def refresh(self):
        self.browser.refresh()

    def get_current_url(self):
        return self.browser.current_url

    def get_title(self):
        return self.browser.title

    def save_screenshot(self, filename: str):
        filename = filename + str(time.time())
        self.browser.save_screenshot(filename + ".png")