'''

    dn.api
    ~~~~~~~~~~~~~~~~~

    This module contains the API classes and method to parse information from
    the Democracy Now website.

'''
# from scraper import (get_shows, get_show_videos, get_web_exclusive_media)
import scraper


class DN(object):
    '''The main API object. Useful as a starting point to get available
    movies.
    '''

    def __init__(self):
        pass

    def get_shows(self):
        '''Returns a list of todays shows.'''
        return [ShowDetails(**show) for show in scraper.get_shows()]

    def get_show_items(self, url):
        '''Returns a list of todays shows.'''
        return [Show(**info) for info in scraper.get_show_videos(url)]

    def get_web_exclusive_media(self,url):
        '''Returns the video from a web exclusive page.'''
        media = scraper.get_web_exclusive_media(url)
        return  Media(**media)


class Media(object):

    def __init__(self, type, url, **kwargs):
        self.type = type
        self.url = url
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Media Url '%s'>" % self.url

class ShowDetails(object):

    def __init__(self, title, url, **kwargs):
        self.title = title
        self.url = url
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Show Date'%s'>" % self.title

class Show(object):

    def __init__(self, url, media_type=None, title=None, poster_url=None, summary=None,**kwargs):
        self.url = url
        self.media_type = media_type
        self.title = title
        self.poster_url = poster_url
        self.summary = summary
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Show '%s'>" % self.title

class WeeklyArchive(object):

    def __init__(self, url, title=None,**kwargs):
        self.url = url
        self.title = title
        self._loaded = False

    @classmethod
    def from_url(cls, url):
        return cls(url=url)

    def __repr__(self):
        return u"<Weekly Archive '%s'>" % self.title




