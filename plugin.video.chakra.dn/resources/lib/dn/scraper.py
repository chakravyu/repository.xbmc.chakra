'''
    nfdc.scraper
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains some functions which do the website scraping for the
    API module. You shouldn't have to use this module directly.
'''
import logging
import re,json,os
from urllib2 import urlopen
import urllib
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup as BS

# setup loggin for debugging
#logging.basicConfig(level=logging.INFO)
max_page = 0


BASE_URL = 'http://m.democracynow.org'
def _url(path):
    '''Returns a full url for the given path'''
    return urljoin(BASE_URL, path)


def get(url):
    '''Performs a GET request for the given url and returns the response'''
    conn = urlopen(url)
    resp = conn.read()
    conn.close()
    return resp


def _html(url):
    '''Downloads the resource at the given url and parses via BeautifulSoup'''
    return BS(get(url), convertEntities=BS.HTML_ENTITIES)


def get_todays_show_videos():
    '''Return  a list of videos from daily shows. Each show is a dict with
    keys of 'name' and 'url'.
    '''    
    
    html = _html(BASE_URL)
    
    # retrieve all the news item links
    shows = html.findAll('li',
        {'class': lambda attr_value: attr_value is not None
                                    and attr_value.startswith('news_item')
                                    and len(attr_value) >= len('news_item')})
    
    items = []

    urls = set()

    for show in shows:
        
        # div which contains the video link and poster link
        video_holder = show.find('div',
            {'class': lambda attr_value: attr_value is not None
                                        and attr_value == 'video_holder'})
        # retrieve video link and replace ipod (low res) link with flash (higher res)
        video_link = video_holder.a['href'].replace('ipod', 'flash')

        logging.info("video_link : " + video_link)

        # retrieve video poster link
        video_poster_link = video_holder.img['src']

        # in the case that the poster path is relative (e.g. for full show)
        if video_poster_link.startswith('/') :
            video_poster_link = _url(video_poster_link)

        logging.info("video_poster_link : " + video_poster_link)

        # retrieve video title
        video_title = show.find('a',
            {'href': lambda attr_value: attr_value is not None
                                        and (attr_value.startswith('/headlines')
                                            or attr_value.startswith('/stories'))})
        
        # in the case of the full show there is no title
        if video_title :
            video_title_text = video_title.string.replace('\n', '')
        else :
            video_title_text = 'Full Show'

        logging.info("video_title_text : " + video_title_text)
        
        items.append({
            'title': video_title_text,
            'url': video_link,
            'poster_url' : video_poster_link
        })

    return [item for item in items if item['title'] and item['url']]






