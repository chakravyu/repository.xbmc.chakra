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

	# def test_api_get_shows(self):
	# 	shows = api.get_shows()
	# 	for show in shows:
	# 		logging.info("show title : " + show.title)
	# 		logging.info("show url : " + show.url)
	# 		show_items = api.get_show_items(show.url)
	# 		for show_item in show_items:
	# 			logging.info("show item url : " + show_item.url)
	# 			logging.info("show item media type : " + show_item.media_type)
	# 			logging.info("show item title : " + show_item.title)
	# 			logging.info("show item poster url : " + show_item.poster_url)
	# 			logging.info("show item summary : " + show_item.summary)
	# 			logging.info('\n')

	def test_api_get_webex_items(self):
		webex_items = api.get_story_items('/categories/weekly_column/1')
		for show_item in webex_items:

			logging.info("story item path : " + show_item.url)
			logging.info("story item media type : " + show_item.media_type)
			logging.info("story item title : " + show_item.title)
			logging.info("story item poster url : " + show_item.poster_url)
			logging.info("story item summary : " + show_item.summary)

			story_video_url = get_story_video_url(show_item.url)
			logging.info("story item url : " + story_video_url)
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

	# def test_api_get_web_exclusive_media(self):
	# 	web_exclusive = api.get_web_exclusive_media('https://www.democracynow.org/2017/6/7/flyers_rights_pres_trump_plan_to')
	# 	logging.info("web exclusive media type : " + web_exclusive.type)
	# 	logging.info("web exclusive media url : " + web_exclusive.url)
	# 	logging.info('\n')

if __name__ == '__main__':
	unittest.main()