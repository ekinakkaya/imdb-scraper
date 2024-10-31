import csv
import os
import time
import requests
import uuid
from bs4 import BeautifulSoup
from lxml import etree 
from fake_useragent import UserAgent



class MovieDataScraper:
    
    def __init__(self) -> None:
        self.user_agent = UserAgent()

        self.csv_file = f"./csv_files/{uuid.uuid4()}.csv"
        self.data_headers = ["name", "description", "duration", "imdb_rating", "metascore", "directors", "writers", "stars"]

        with open(self.csv_file, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data_headers)
            writer.writeheader()


    def read_all_files_in_directory(self, directory_path):
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        
    def get_page(self, url):
        headers = {
            'User-Agent': self.user_agent.random,
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response
            elif response.status_code in [403, 429]:
                print("banned or rate-limited. waiting for 60 secs")
                time.sleep(60)  # wait a minute and retry
                headers["User-Agent"] = self.user_agent.random
            else:
                print("network error. response status code: " + response.status_code)
                time.sleep(10)
    
    
    def write_movie_data_to_csv(self, movie_data):
        with open(self.csv_file, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data_headers)
            writer.writerow(movie_data)


    def scrape_movie_data_from_file(self, filepath):
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines()]

            for url in lines:
                print(url)
                page = self.get_page(url)

                soup = BeautifulSoup(page.content, "html.parser")
                
                dom = etree.HTML(str(soup))


                movie_name_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span"
                movie_name = dom.xpath(movie_name_xpath)[0].text

                movie_description_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[2]"
                movie_description = dom.xpath(movie_description_xpath)[0].text

                movie_duration_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]"
                try:
                    movie_duration = dom.xpath(movie_duration_xpath)[0].text
                except IndexError:
                    movie_duration = "N/A"
                    

                movie_imdb_rating_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]"
                movie_imdb_rating = dom.xpath(movie_imdb_rating_xpath)[0].text

                movie_metascore_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[3]/a/span/span[1]/span"
                try:
                    movie_metascore = dom.xpath(movie_metascore_xpath)[0].text
                except:
                    movie_metascore = "N/A"

                movie_directors_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul"
                movie_directors_list = dom.xpath(movie_directors_list_xpath)[0]
                directors = [director[0].text for director in movie_directors_list]

                movie_writers_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul"
                movie_writers_list = dom.xpath(movie_writers_list_xpath)[0]
                writers = [writer[0].text for writer in movie_writers_list]

                movie_stars_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul"
                movie_stars_list = dom.xpath(movie_stars_list_xpath)[0]
                stars = [star[0].text for star in movie_stars_list]

                #movie_genres_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/ul[2]/li[1]/div/ul"
                #movie_genres_list = dom.xpath(movie_genres_list_xpath)[0]
                #for genre_element in movie_genres_list:
                #    print("star: " + genre_element[0].text)

                #movie_release_date_xpath = "//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[1]/div/ul/li/a"
                #movie_release_date = dom.xpath(movie_release_date_xpath)[0].text
                #print(movie_release_date)

                movie_data = {
                    "name": movie_name,
                    "description": movie_description,
                    "duration": movie_duration,
                    "imdb_rating": movie_imdb_rating,
                    "metascore": movie_metascore,
                    "directors": directors,
                    "writers": writers,
                    "stars": stars
                }

                self.write_movie_data_to_csv(movie_data)




    
    def scrape_movie_data_from_directory(self, directory_path = "./movie_links"):
        files = self.read_all_files_in_directory(directory_path)

        for file in files:
            print(file)
            self.scrape_movie_data_from_file(os.path.join(directory_path, file))

        pass


    