'''

    dn.api
    ~~~~~~~~~~~~~~~~~

    This module contains the API classes and method to parse information from
    the Democracy Now website.

'''
from scraper import (get_todays_show_videos)


class DN(object):
    '''The main API object. Useful as a starting point to get available
    movies.
    '''

    def __init__(self):
        pass

    def get_todays_shows(self):
        '''Returns a list of todays shows.'''
        return [Show(**info) for info in get_todays_show_videos()]


class Show(object):

    def __init__(self, url, title=None, poster_url=None,**kwargs):
        self.url = url
        self.title = title
        self.poster_url = poster_url
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Show '%s'>" % self.title




