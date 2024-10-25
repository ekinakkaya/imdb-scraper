from imdb_scraper.config import LOGGING_LEVEL

from imdb_scraper.imdb_scraper import IMDBLinkScraper

from imdb_scraper.logger import Logger

if __name__ == "__main__":
    scraper = IMDBLinkScraper()

    #yearly_counts_data = scraper.fetch_yearly_movie_count(2000, 2024)
    #scraper.create_scrape_path_from_yearly_counts("yearly_counts.json")
    scraper.scrape_movies_from_scrape_path("scrape_path.json")