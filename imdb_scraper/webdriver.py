from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from imdb_scraper.logger import globalLoggerInstance

class CustomWebDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        self.logger = globalLoggerInstance
        
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
        options.add_argument("--no-sandbox")  # Useful in some environments
        options.add_argument("--disable-dev-shm-usage")  # Prevent memory issues
        options.add_argument("--disable-extensions")  # Disable extensions
        options.add_argument("--disable-infobars")  # Disable info bars
        options.add_argument("--disable-notifications")  # Disable notifications
        options.add_argument("--disable-popup-blocking")  # Disable popup blocking
        options.add_argument("--disable-translate")  # Disable translation

        super().__init__(options=options, *args, **kwargs)
         
    def navigate(self, url):
        self.get(url)
        self.logger.info("navigated to " + url)