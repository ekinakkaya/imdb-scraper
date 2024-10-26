from imdb_scraper.logger import globalLoggerInstance

from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

import datetime
import json
import os
import time

from imdb_scraper.webdriver_manager import WebDriverManager

class IMDBLinkScraper:
    root_search_url = "https://www.imdb.com/search/title/?"

    # we will add this to the link with the formatting: ?release_date=2024-10-03,2024-10-03
    release_date_query = "&release_date="
    scraped_imdb_movie_links = []
    yearly_counts_file_path = "yearly_counts.json"
    
    def __init__(self):
        self.logger = globalLoggerInstance
        self.logger.info("starting IMDB Link scraper")
        self.driverManager = WebDriverManager()
        self.driver = None

    @property
    def driver(self):
        return self.driverManager.getDriver()

    @driver.setter
    def driver(self, driver):
        self.driverManager.driver = driver


    def create_search_query(self, start_date, end_date):
        return self.root_search_url + self.release_date_query + start_date + "," + end_date


    def read_yearly_movie_counts_file(self, filename):
        data_normalized = {}

        with open(filename, "r") as file:
            data = json.load(file)

            # we normalize the date while reading the file
            data_normalized["updated_at"] = datetime.datetime.strptime(data["updated_at"], "%Y-%m-%d")
            data_normalized["yearly_counts"] = {}

            for year in data["yearly_counts"]:
                data_normalized["yearly_counts"][year] = data["yearly_counts"][year]
        
        return data_normalized


    def write_yearly_movie_counts_file(self, filename, updated_at: any, yearly_counts):
        today = datetime.datetime.now().strftime("%Y-%m-%d")

        data_structured = {
            "updated_at": today,
            "yearly_counts": yearly_counts
        }

        with open(filename, "w") as file:
            self.logger.info("writing the yearly movie counts to JSON file: " + filename + " with indent=2. updated_at=" + updated_at)
            json.dump(data_structured, file, indent=2)


    # from 1800 to this day, fetch how many movies are there in every year
    # this is for understanding the data and how we should proceed fetching it
    def fetch_yearly_movie_count(self, start_year: int, end_year: int):
        self.driverManager.init_driver()
        # if a yearly_counts.json file exists and it is not older than 7 days, we just return the yearly_counts

        if (os.path.exists(self.yearly_counts_file_path)):
            self.logger.info("a yearly_counts.json file already exists. checking if it is viable")

            data = self.read_yearly_movie_counts_file(self.yearly_counts_file_path)

            updated_at = data["updated_at"] # this is already in datetime format
            now = datetime.datetime.now()
            seven_days_ago = now - datetime.timedelta(days=7)

            if updated_at > seven_days_ago:
                if str(start_year) in data["yearly_counts"] and str(end_year) in data["yearly_counts"]:
                    self.logger.info("yearly_counts.json file is viable. returning the data")
                    return data
                else:
                    self.logger.warning("yearly_counts.json file does not contain the needed years. going to start fetching new data")
            else:
                self.logger.info("yearly_counts.json file is older than 7 days. going to start fetching new data")
        else:
            self.logger.info("yearly_counts.json file does not exist. going to start fetching it")
            
                
        yearly_counts: dict = {}
        
        for year in range(start_year, end_year + 1):
            movie_count: int = 0
            
            start_date = str(year) + "-01-01"
            end_date = str(int(year + 1)) + "-01-01"

            self.logger.info("fetching movie count for interval: " + start_date + " | " + end_date)

            self.driverManager.navigate(self.create_search_query(start_date, end_date))
            self.driver.implicitly_wait(10)

            movie_count_element_list = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[1]/div[1]")
            if (movie_count_element_list != []):
                movie_count_text: str = movie_count[0].text
                if movie_count_text == "":
                    movie_count = 0
                else:
                    movie_count = int(movie_count.split("of ")[1].replace(",", ""))
                
                print("movie count for year " + str(year) + ": " + str(movie_count))
                self.logger.info("found movie count for interval: " + start_date + " | " + end_date + " is " + str(movie_count))
            else:
                movie_count = 0
                print("movie count unknown for year " + str(year))
                self.logger.warning("movie count unknown for year " + str(year))

            yearly_counts[year] = movie_count

        self.logger.info("finished fetching movie counts for years " + str(start_year) + " to " + str(end_year))

        self.write_yearly_movie_counts_file(self.yearly_counts_file_path, yearly_counts)

        self.driver.quit()


    def create_scrape_path_from_yearly_counts(self, yearly_counts_filename=yearly_counts_file_path):
        data = self.read_yearly_movie_counts_file(yearly_counts_filename)

        scrape_path = []
        
        for year in data["yearly_counts"]:
            if data["yearly_counts"][year] > 500000:
                print("the year " + year + " should be scraped daily")

                start_date = datetime.datetime(int(year), 1, 1)
                delta = datetime.timedelta(days=1)
                end_date = datetime.datetime(int(year) + 1, 1, 1) - delta # last day of the year
                
                current_date = start_date
                while current_date < end_date:
                    next_date = current_date + delta
                    day = current_date.strftime("%Y-%m-%d")
                    scrape_path.append(day + "," + day)
                    current_date = next_date

            elif data["yearly_counts"][year] > 50000:
                print("the year " + year + " should be scraped monthly")

                for month in range(1, 13):
                    start_date = datetime.datetime(int(year), month, 1)

                    if month == 12:
                        end_date = datetime.datetime(int(year) + 1, 1, 1) - datetime.timedelta(days=1)
                    else:
                        end_date = datetime.datetime(int(year), month + 1, 1) - datetime.timedelta(days=1)

                    scrape_path.append(start_date.strftime("%Y-%m-%d") + "," + end_date.strftime("%Y-%m-%d"))
            elif data["yearly_counts"][year] > 0:
                print("the year " + year + " should be scraped yearly")
                scrape_path.append(year + "-01-01," + year + "-12-31")
            else:
                print("the year " + year + " should not be scraped")

        self.write_scrape_path_to_json(scrape_path)

        self.logger.info("created scrape path from yearly counts")
        
        return scrape_path


    def write_scrape_path_to_json(self, scrape_path):
        data_structured = {
            "scrape_path_total_count": len(scrape_path),
            "scrape_path_entries": {
            }
        }

        for i in range(len(scrape_path)):
            data_structured["scrape_path_entries"][i] = scrape_path[i]

        with open("scrape_path.json", "w") as file:
            self.logger.info("writing the scrape path to JSON file: scrape_path.json")
            json.dump(data_structured, file, indent=2)


    def read_scrape_path_from_file(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            
            scrape_path = []
            
            for i in range(data["scrape_path_total_count"]):
                scrape_path.append(data["scrape_path_entries"][str(i)])
            return scrape_path

        return []
        

    # we close the preferences popup by clicking the decline button
    # has this xpath
    # //*[@id="__next"]/div/div/div[2]/div/button[1]
    def close_bad_imdb_popup(self):
        self.logger.info("closing the bad IMDB popup if exists")
        decline_button = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/div/div/div[2]/div/button[1]")

        if len(decline_button) > 0:
            decline_button[0].click()
            self.logger.info("closed the bad imdb preferences popup, waiting for 2 secs")
            time.sleep(2)
        
        
    def write_movie_links_to_file(self, start_date, end_date, movies):
        with open(str(start_date) + "_" + str(end_date) + "_" + datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + ".imdb_scraper.txt", "a") as file:
            for movie in movies:
                # remove the ?ref_=sr_t_1 stuff
                movie_link = movie.get_attribute("href").split("?")[0]
                file.write(movie_link + "\n")


    def scrape_movie_links_in_interval(self, start_date, end_date, movie_count):
        clicks_needed = int(movie_count / 50) + 1
        self.logger.info("we will click " + str(clicks_needed) + " times to get all the movies")

        # we click the see more button until it disappears
        count_fifty_more_clicked = 0
        
        # TODO: we are doing 2 loops here, in fact we can do this with just one. fix it
        while True:
            more_button_list = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button")
            if len(more_button_list) == 0:
                self.logger.info("could not found the 50 more button. we probably have all the movies now.")

                # find all the movies in the page and get their links
                self.logger.info("finding all the movie links")
                movies = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/ul/li/div/div/div/div[1]/div[2]/div[1]/a")
                self.write_movie_links_to_file(start_date, end_date, movies)
                break

            else:
                try:
                    more_button_list = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button")
                    if more_button_list == []:
                        pass

                    element_position = self.driver.execute_script("return arguments[0].getBoundingClientRect().top;", more_button_list[0])
                    self.driver.execute_script("window.scrollBy(0, arguments[0] - 200);", element_position)
                    time.sleep(1)

                    self.logger.info("clicking the '50 more' button")
                    more_button_list[0].click()

                    count_fifty_more_clicked += 1
                    self.logger.info("clicked " + str(count_fifty_more_clicked) + " times. [" + str(count_fifty_more_clicked) + "/" + str(clicks_needed) + "] | {" + start_date + ", " + end_date + "}")

                    time.sleep(1)
                    self.driver.implicitly_wait(2)
                except StaleElementReferenceException:
                    self.logger.warning("stale element reference exception. Retrying...")
                    time.sleep(2)
                except:
                    self.logger.info("could not click the '50 more' button. scrolling to it.")
                    element_position = self.driver.execute_script("return arguments[0].getBoundingClientRect().top;", more_button_list[0])
                    self.driver.execute_script("window.scrollBy(0, arguments[0] - 200);", element_position)
                    time.sleep(2)
                
        
    def find_movie_count_in_page(self, start_date, end_date):
        movie_count_element_list = self.driver.find_elements(by=By.XPATH, value="//*[@id=\"__next\"]/main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[1]/div[1]")
        movie_count: int = 0
        if movie_count_element_list == []:
            self.logger.warning("movie count unknown for interval. will default to 0." + start_date + ", " + end_date)
            return 0

        movie_count_text = movie_count_element_list[0].text
        if movie_count_text == "":
            movie_count = 0
        else:
            movie_count = int(movie_count_text.split("of ")[1].replace(",", ""))
            self.logger.info("movie count for interval: " + start_date + " | " + end_date + " is " + str(movie_count))
        
        return movie_count
    
    
    def scrape_movies_from_scrape_path(self, scrape_path_filename):
        scrape_path = self.read_scrape_path_from_file(scrape_path_filename)
        self.driverManager.init_driver()

        for interval in scrape_path:
            self.logger.info("starting scraping movies from time interval: " + interval)
            start_date, end_date = interval.split(",")
            self.driver.navigate(self.create_search_query(start_date, end_date))
            self.driver.implicitly_wait(5)
            time.sleep(3)

            self.close_bad_imdb_popup()

            movie_count: int = self.find_movie_count_in_page(start_date, end_date)

            if movie_count != 0:
                self.scrape_movie_links_in_interval(start_date, end_date, movie_count)
