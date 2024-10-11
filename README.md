# IMDb Scraper

This is a web scraper for fetching ALL the movie information in the IMDb database. This project is the revamped version of the one I have made before. You can check that one out [here](https://github.com/ekinakkaya/movies-data-scraping).

# plan

- first we get all the movie page links. here's how we do it:
  - go to advanced search
  - search for a release date interval
    - the date interval should be defaulted to one month but in the early years like 1980 there are not many movies, so we should increase the interval to reduce scraping time
    - first we can scrape every month for only the total movie number
  - find and save all the links