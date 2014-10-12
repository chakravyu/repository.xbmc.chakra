'''
    dn.scraper
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


def get_todays_show_videos(show_date_url):
    '''Return  a list of videos from daily shows. Each show is a dict with
    keys of 'name' and 'url'.
    '''    
    if show_date_url == '':
        html = _html(BASE_URL)
    else :
        html = _html(show_date_url)
    
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
        if video_holder:
            # retrieve video link and replace ipod (low res) link with flash (higher res)
            video_link = video_holder.a['href'].replace('ipod', 'flash')
        
            # retrieve video poster link
            video_poster_link = video_holder.img['src']            
        else:
            video_holder = show.find('a',
                {'class': lambda attr_value: attr_value is not None
                                            and attr_value == 'video_link'})
            video_link = _url(video_holder['href'])
            video_poster_link = video_holder.img['src'] 

        logging.info("video_link : " + video_link)

        # in the case that the poster path is relative (e.g. for full show)
        if video_poster_link.startswith('/') :
            video_poster_link = _url(video_poster_link)
        logging.info("video_poster_link : " + video_poster_link)

        # retrieve video title
        video_title = show.find('a',
            {'href': lambda attr_value: attr_value is not None
                                        and (attr_value.startswith('/headlines')
                                        or attr_value.startswith('/stories')
                                        or attr_value.startswith('/web_exclusives'))})
        
        # in the case of the full show there is no title
        if video_title :
            if video_title.string:
                video_title_text = video_title.string.replace('\n', '')
            else:
                video_title_text = video_holder.img['alt']
        else :
            video_title_text = 'Full Show'

        logging.info("video_title_text : " + video_title_text)

        # retrieve video title
        video_summary = show.find('div',
            {'class': lambda attr_value: attr_value is not None
                                        and attr_value == 'more_summary'})
        video_summary_p = None

        if video_summary :
            video_summary_p = video_summary.find('p')

        if video_summary_p :
            if video_summary_p.string:
                video_summary_text = video_summary_p.string.replace('\n', '')
            else:
                video_summary_text = 'Nested tags in summary. Ignoring for now'
        else :
            video_summary_text = ''
        logging.info("video_summary_text : " + video_summary_text + '\n')

        items.append({
            'title': video_title_text,
            'url': video_link,
            'poster_url' : video_poster_link,
            'summary' : video_summary_text
        })

    return [item for item in items if item['title'] and item['url']]

def get_weekly_archive_links():
    html = _html(BASE_URL)
    
    # retrieve all the news item links
    weekly_archives = html.findAll('div',
        {'class': lambda attr_value: attr_value is not None
                                    and attr_value == 'context_header previous_show'})
    
    items = []

    for weekly_archive in weekly_archives:
        weekly_archive_text = weekly_archive.find('h2').string.replace('\n', '')
        logging.info("weekly_archive_text : " + weekly_archive_text)

        weekly_archive_onclick = weekly_archive['onclick']
        start_index = weekly_archive_onclick.find('\'',0)
        end_index = weekly_archive_onclick.find('?',start_index)

        weekly_archive_url = _url(weekly_archive_onclick[start_index+1:end_index])
        logging.info("weekly_archive_url : " + weekly_archive_url)

        items.append({
            'title': weekly_archive_text,
            'url': weekly_archive_url,            
        })

    return [item for item in items if item['title'] and item['url']]

def get_web_exclusives(page):
    '''Returns a list of web exclusive videos. 
    '''

    url = _url('/categories/19?page=' + str(page))    
    return get_todays_show_videos(url)






