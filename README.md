# IMDb Scraper

This is a web scraper for fetching ALL the movie information in the IMDb database. This project is the revamped version of the one I have made before. You can check that one out [here](https://github.com/ekinakkaya/movies-data-scraping).

# todo

- [x] scrape movie counts for every year
- [x] scrape movie links
- [x] fix the unclickable button issues
- [x] refactor the code a bit
- [x] web driver manager
- [x] properly handle where will links be saved and in what format.
- [x] make it keep going where it left off by tracking movie_links and scrape_path
- [x] implement movie data scraper
- [ ] add logger to the movie data scraper
- [ ] make tests
- [ ] progress bar
- [ ] there is no failsafe for being banned from the site. test this and evaluate
- [ ] add session logic for unexpected closes, crashs, network issues, etc. so the program can keep scraping where it has left off
- [ ] webpage manager
- [x] ~~session manager~~

# bugs

- with this method were getting a FEW of N/A's. we might have to use selenium
```
Traceback (most recent call last):
  File "C:\Users\ekin_\projeler\imdb-scraper\main.py", line 12, in <module>
    movie_data_scraper.scrape_movie_data_from_directory()
  File "C:\Users\ekin_\projeler\imdb-scraper\imdb_scraper\movie_data_scraper.py", line 134, in scrape_movie_data_from_directory
    self.scrape_movie_data_from_file(os.path.join(directory_path, file))
  File "C:\Users\ekin_\projeler\imdb-scraper\imdb_scraper\movie_data_scraper.py", line 100, in scrape_movie_data_from_file
    movie_stars_list = dom.xpath(movie_stars_list_xpath)[0]
                       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
```