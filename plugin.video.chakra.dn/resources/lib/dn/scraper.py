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
    elif show_date_url.startswith('/') :
        html = _html(_url(show_date_url))
    else:
        html = _html(show_date_url)
    
    # retrieve all the news item links
    shows = html.findAll('li',
        {'class': lambda attr_value: attr_value is not None
                                    and attr_value.startswith('news_item')
                                    and len(attr_value) >= len('news_item')})
    
    items = []

    urls = set()

    for show in shows:
        title = ''
        media_url = ''
        media_type = ''
        poster = ''
        summary = ''

        # div which contains the video link and poster link
        video_tag = show.find('a',
            {'href': lambda attr_value: attr_value is not None
                                        and (attr_value.find('.mp4') != -1)})
        video = None
        if video_tag:
            # retrieve video link and replace ipod (low res) link with flash (higher res)     
            video = video_tag['href'].replace('ipod', 'flash')
            # in the case that the video link path is relative 
            if video.startswith('/') :
                video = _url(video)
            logging.info("video : " + video)

        # div which contains the audio link and poster link
        audio_tag = show.find('a',
            {'href': lambda attr_value: attr_value is not None
                                        and (attr_value.find('.mp3') != -1)})        
        audio = None
        if audio_tag:
            audio = audio_tag['href']
            # in the case that the audio link path is relative 
            if audio.startswith('/') :
                audio = _url(audio)       

            logging.info("audio : " + audio)


        # div which contains the audio link and poster link
        poster_tag = show.find('img',
            {'src': lambda attr_value: attr_value is not None
                                        and (attr_value.find('.jpg') != -1
                                            or (attr_value.find('.jpeg') != -1))})
        poster = None
        if poster_tag:
            poster = poster_tag['src']
            # in the case that the audio link path is relative 
            if poster.startswith('/') :
                poster = _url(poster)           
            logging.info("poster : " + poster)

        # retrieve title
        title_tag = show.find('a',
            {'href': lambda attr_value: attr_value is not None
                                        and (attr_value.startswith('/headlines')
                                        or attr_value.startswith('/stories')
                                        or attr_value.startswith('/web_exclusives'))})
        if not title_tag:
            title_tags = show.findAll('a',
                {'href': lambda attr_value: attr_value is not None                                            
                                            and attr_value.startswith('/columns')})
            if title_tags and len(title_tags) >= 2:
                title_tag = title_tags[1]

        title = ''
        # in the case of the full show there is no title
        if title_tag :
            if title_tag.text:
                title = title_tag.text.replace('\n', '')
            elif video_tag and 'alt' in video_tag:
                    title = video_tag['alt']
            elif poster_tag and 'alt' in poster_tag:
                    title = poster_tag['alt']
        else :
            title = 'Full Show'

        

        

        # retrieve video title
        summary_tag = show.find('div',
            {'class': lambda attr_value: attr_value is not None
                                        and attr_value == 'more_summary'})
        summary_tag_p = None

        if summary_tag :
            summary_tag_p = summary_tag.find('p')

        if summary_tag_p:            
            summary = summary_tag_p.text.replace('\n', '')            
        else :
            summary = ''
        logging.info("summary : " + summary)
        
        if title == '' and summary != '':
            title = summary[:40] + '...'

        logging.info("title : " + title)

        media_type = 'video'
        if video:
            media_url = video            
        elif audio:
            media_url = audio            
        else:                        
            title = '[News]' + title 
            media_url = ''

        logging.info("media_type : " + media_type)

        items.append({
            'title': title,
            'url': media_url,
            'media_type' : media_type,
            'poster_url' : poster,
            'summary' : summary
        })
        logging.info('\n')

    return [item for item in items if (item['url'] and item['media_type']) 
                    or item['title'] or item['summary']]

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






