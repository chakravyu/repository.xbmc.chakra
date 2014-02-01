'''

    nfdc.api
    ~~~~~~~~~~~~~~~~~

    This module contains the API classes and method to parse information from
    the NFDC (CinemasOfIndia) website.

'''
from scraper import (get_movies,get_max_page,get_movie_stream)


class NFDC(object):
    '''The main API object. Useful as a starting point to get available
    movies.
    '''

    def __init__(self):
        pass

    def get_movies(self,page):
        '''Returns a list of movies available on the website.'''
        return [Movie(**info) for info in get_movies(page)]

    def get_max_page(self):
        '''Returns the maximum number of pages.'''
        return get_max_page()

    def get_movie_stream(self,url):
        '''Returns the url of the movie stream hosted on the 
           movie site referred to by the input url
        '''
        return get_movie_stream(url)
        



class Movie(object):

    def __init__(self, url, name=None, **kwargs):
        self.url = url
        self._name = name
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Movie '%s'>" % self.name

    @property
    def name(self):
        if not self._name:
            self._load_metadata()
        return self._name



