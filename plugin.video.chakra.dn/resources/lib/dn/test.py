from scraper import *
from api import DN
import unittest
import logging

logging.basicConfig(level=logging.INFO)

api = DN()


class DNTest(unittest.TestCase):

    # def test_api_get_show_videos(self):
		# show_items = api.get_todays_shows('https://www.democracynow.org/shows/2017/6/6')
		# for show_item in show_items:
		# 	logging.info("show item url : " + show_item.url)
		# 	logging.info("show item media type : " + show_item.media_type)
		# 	logging.info("show item title : " + show_item.title)
		# 	logging.info("show item poster url : " + show_item.poster_url)
		# 	logging.info("show item summary : " + show_item.summary)
		# 	logging.info('\n')

	def test_api_get__shows(self):
		shows = api.get_shows()
		for show in shows:
			logging.info("show title : " + show.title)
			logging.info("show url : " + show.url)
			show_items = api.get_todays_shows(show.url)
			for show_item in show_items:
				logging.info("show item url : " + show_item.url)
				logging.info("show item media type : " + show_item.media_type)
				logging.info("show item title : " + show_item.title)
				logging.info("show item poster url : " + show_item.poster_url)
				logging.info("show item summary : " + show_item.summary)
				logging.info('\n')



	# def test_scraper_get_todays_show_videos(self):
	# 	get_todays_show_videos('')
    #
	# def test_scraper_get_archive_show_videos(self):
	# 	get_todays_show_videos('http://m.democracynow.org/shows_include/2014/10/14')
    #
	# def test_scraper_get_weekly_archive_links(self):
	# 	get_weekly_archive_links()
    #
	# def test_scraper_get_web_exclusives(self):
	# 	get_todays_show_videos('/categories/19?page=1')

if __name__ == '__main__':
	unittest.main()