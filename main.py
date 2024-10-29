from imdb_scraper.imdb_scraper import IMDBLinkScraper

if __name__ == "__main__":
    scraper = IMDBLinkScraper()

    #yearly_counts_data = scraper.fetch_yearly_movie_count(1800, 2025)
    #scraper.create_scrape_path_from_yearly_counts("yearly_counts.json")
    scraper.scrape_movies_from_scrape_path("scrape_path.json")