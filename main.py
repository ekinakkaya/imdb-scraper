from imdb_scraper.config import LOGGING_LEVEL
from imdb_scraper.imdb_scraper import IMDBLinkScraper

if __name__ == "__main__":
    # we should import the scraper and fire up the thing
    scraper = IMDBLinkScraper()
    #yearly_counts_data = scraper.fetch_yearly_movie_count(2000, 2024)
    #scraper.create_scrape_path_from_yearly_counts("yearly_counts.json")
    scraper.scrape_movies_from_scrape_path("scrape_path.json")