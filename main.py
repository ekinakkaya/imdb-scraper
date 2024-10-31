from imdb_scraper.imdb_scraper import IMDBLinkScraper
from imdb_scraper.movie_data_scraper import MovieDataScraper

if __name__ == "__main__":
    link_scraper = IMDBLinkScraper()
    movie_data_scraper = MovieDataScraper()

    #yearly_counts_data = scraper.fetch_yearly_movie_count(1800, 2025)
    #scraper.create_scrape_path_from_yearly_counts("yearly_counts.json")
    #link_scraper.scrape_movies_from_scrape_path("scrape_path.json")

    movie_data_scraper.scrape_movie_data_from_directory()
