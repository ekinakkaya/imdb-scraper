# logger for writing log records to a file
import logging

class Logger:
    def __init__(self, filename):
        logging.basicConfig(
            filename=filename,
            encoding="utf-8",
            level=logging.DEBUG,
            format="%(asctime)s || %(levelname)s || %(name)s || %(funcName)s || %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("logger initialized")

    def getLogger(self):
        return self.logger