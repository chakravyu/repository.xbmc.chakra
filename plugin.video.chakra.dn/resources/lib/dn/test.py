from scraper import (get_todays_show_videos)
from api import DN
import unittest
import logging

logging.basicConfig(level=logging.INFO)

api = DN()

class DNTest(unittest.TestCase):

	def test_api_get_todays_shows(self):
		api.get_todays_shows()

	def test_scraper_get_todays_show_videos(self):
		get_todays_show_videos()


if __name__ == '__main__':
    unittest.main()