from selenium import webdriver
from selenium.webdriver.chrome.options import Options

### if you want to make CI/CD pipeline

# def get_configured_chrome_driver():
#     options = Options()
#     options.add_experimental_option('detach', True)
#     options.add_argument('--guest')
#     options.add_argument("--lang=hu")
#     options.add_argument("--headless")
#     browser = webdriver.Chrome(options=options)
#     browser.set_window_size(1920, 1080)
#     return browser


def get_configured_chrome_driver():
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_argument('--guest')
    options.add_argument("--lang=hu")
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    return browser