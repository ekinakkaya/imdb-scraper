from imdb_scraper.webdriver import CustomWebDriver

from selenium.webdriver.support.ui import WebDriverWait

from imdb_scraper.logger import globalLoggerInstance

class WebDriverManager:

    def __init__(self):
        self.DRIVER_INITIATED = False
        
        self.driver = None
        self.logger = globalLoggerInstance

    def getDriver(self):
        return self.driver

    def init_driver(self):
        if self.DRIVER_INITIATED:
            return

        self.logger.info("initializing selenium webdriver.")
        self.driver = CustomWebDriver()
        self.driver.wait = WebDriverWait(self.driver, 5)
            
        self.logger.info("initialized selenium webdriver with " + self.driver.name + " driver.")
        self.DRIVER_INITIATED = True

        return self.driver
