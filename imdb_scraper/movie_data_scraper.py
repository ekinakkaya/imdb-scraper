import os
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree 



class MovieDataScraper:
    
    def __init__(self) -> None:
        pass


    def read_all_files_in_directory(self, directory_path):
        return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]


    def scrape_movie_data_from_file(self, filepath):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file.readlines()]

            for url in lines:
                print(url)
                page = requests.get(url, headers=headers)

                soup = BeautifulSoup(page.content, "html.parser")
                
                dom = etree.HTML(str(soup))

                movie_name_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span"
                movie_name = dom.xpath(movie_name_xpath)[0].text
                print(movie_name)

                movie_description_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[2]"
                movie_description = dom.xpath(movie_description_xpath)[0].text
                print(movie_description)

                movie_duration_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]"
                movie_duration = dom.xpath(movie_duration_xpath)[0].text
                print(movie_duration)

                movie_imdb_rating_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/a/span/div/div[2]/div[1]/span[1]"
                movie_imdb_rating = dom.xpath(movie_imdb_rating_xpath)[0].text
                print(movie_imdb_rating)

                movie_metascore_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[3]/a/span/span[1]/span"
                movie_metascore = dom.xpath(movie_metascore_xpath)[0].text
                print("metascore: " + movie_metascore)

                movie_directors_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul"
                movie_directors_list = dom.xpath(movie_directors_list_xpath)[0]
                for director_element in movie_directors_list:
                    print("director: " + director_element[0].text)

                movie_writers_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[2]/div/ul"
                movie_writers_list = dom.xpath(movie_writers_list_xpath)[0]
                for writer_element in movie_writers_list:
                    print("writer: " + writer_element[0].text)

                movie_stars_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[3]/div/ul"
                movie_stars_list = dom.xpath(movie_stars_list_xpath)[0]
                for star_element in movie_stars_list:
                    print("star: " + star_element[0].text)

                #movie_genres_list_xpath = "//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/ul[2]/li[1]/div/ul"
                #movie_genres_list = dom.xpath(movie_genres_list_xpath)[0]
                #for genre_element in movie_genres_list:
                #    print("star: " + genre_element[0].text)

                #movie_release_date_xpath = "//*[@id=\"__next\"]/main/div/section[1]/div/section/div/div[1]/section[11]/div[2]/ul/li[1]/div/ul/li/a"
                #movie_release_date = dom.xpath(movie_release_date_xpath)[0].text
                #print(movie_release_date)

                time.sleep(100)



    
    def scrape_movie_data_from_directory(self, directory_path = "./movie_links"):
        files = self.read_all_files_in_directory(directory_path)

        for file in files:
            self.scrape_movie_data_from_file(os.path.join(directory_path, file))

        pass


    