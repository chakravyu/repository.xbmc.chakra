from addon import (clear_cache, get_movie_items)
import unittest
import logging

logging.basicConfig(level=logging.INFO)

class NFDCTest(unittest.TestCase):

    def setUp(self) :
        logging.info("clearing cache")
        clear_cache()

    def test_get_movie_items(self):
        get_movie_items(1)

if __name__ == '__main__':
    unittest.main()