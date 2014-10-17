'''

    dn.api
    ~~~~~~~~~~~~~~~~~

    This module contains the API classes and method to parse information from
    the Democracy Now website.

'''
from scraper import (get_todays_show_videos,get_weekly_archive_links,get_web_exclusives)


class DN(object):
    '''The main API object. Useful as a starting point to get available
    movies.
    '''

    def __init__(self):
        pass

    def get_todays_shows(self, url):
        '''Returns a list of todays shows.'''
        return [Show(**info) for info in get_todays_show_videos(url)]

    def get_weekly_archives(self):
        '''Returns a list of weekly archives.'''
        return [WeeklyArchive(**info) for info in get_weekly_archive_links()]



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




