from scraper import *
from api import DN
import unittest
import logging

logging.basicConfig(level=logging.INFO)

api = DN()

class DNTest(unittest.TestCase):

	def test_api_get_todays_shows(self):
		shows = api.get_todays_shows('')
		for show in shows:
			logging.info("show url : " + show.url)
			logging.info("show media type : " + show.media_type)

	def test_scraper_get_todays_show_videos(self):
		get_todays_show_videos('')

	def test_scraper_get_archive_show_videos(self):
		get_todays_show_videos('http://m.democracynow.org/shows_include/2014/10/14')

	def test_scraper_get_weekly_archive_links(self):
		get_weekly_archive_links()

	def test_scraper_get_web_exclusives(self):
		get_todays_show_videos('/categories/19?page=1')

if __name__ == '__main__':
    unittest.main()