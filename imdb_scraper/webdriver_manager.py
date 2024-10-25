from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from imdb_scraper.logger import globalLoggerInstance

class WebDriverManager:
    DRIVER_INITIATED = False

    def __init__(self):
        self.driver = None
        self.logger = globalLoggerInstance

    def getDriver(self):
        return self.driver

    def init_driver(self):
        if self.DRIVER_INITIATED:
            return

        self.logger.info("initializing selenium webdriver.")
        self.driver = webdriver.Chrome()
        self.driver.wait = WebDriverWait(self.driver, 5)
            
        self.logger.info("initialized selenium webdriver with " + self.driver.name + " driver.")
        self.DRIVER_INITIATED = True

        return self.driver

    def navigate(self, url):
        self.init_driver()
        self.driver.get(url)
        self.logger.info("navigated to " + url)