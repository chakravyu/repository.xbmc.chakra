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
from bs4  import BeautifulSoup as BS


# setup loggin for debugging
logging.basicConfig(level=logging.INFO)
max_page = 0


BASE_URL = 'https://www.democracynow.org/'
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
    return BS(get(url), "html.parser")


def get_show_videos(show_date_url):
    '''
    Return  a list of videos from a particular show. 
    Each show is a dict with show items.
    '''
    html = _html(_url(show_date_url))

    items = []

    urls = set()

    player = html.find('div',
        {'class': lambda attr_value: attr_value is not None
            and attr_value.startswith('daily_show_container')
            and len(attr_value) >= len('daily_show_container')})


    full_show = json.loads(unicode(html.find(id="show_video").contents[0].contents[0]))
    full_show_video = str(full_show['high_res_video'])
    full_show_audio = str(full_show['audio'])
    full_show_img = str(full_show['image'])

    video_content_details = player.find('div',
                {'class': lambda attr_value: attr_value is not None
                    and attr_value.startswith('show_content_details')
                    and len(attr_value) >= len('show_content_details')})


    content_index = 0
    ITEM_URL='url'
    ITEM_TITLE='title'
    ITEM_MEDIA_TYPE='media_type'
    ITEM_POSTER_URL='poster_url'
    ITEM_SUMMARY='summary'

    items.append({
        ITEM_TITLE: 'Full Show',
        ITEM_URL: full_show_video,
        ITEM_MEDIA_TYPE : 'video',
        ITEM_POSTER_URL : full_show_img,
        ITEM_SUMMARY : 'Full Show'
    })
    for content_detail in video_content_details:
        title = ''
        media_url = ''
        poster_url = full_show_img
        summary = ''

        video_description_tag = content_detail.find('div',
                      {'class': lambda attr_value: attr_value is not None
                           and attr_value.startswith('description')
                           and len(attr_value) >= len('description')})
        video_description = video_description_tag.find('a',
                        {'data-player-seek': lambda attr_value: attr_value is not None})
        video_seek = None
        video_title = None
        show_media = full_show_video
        if video_description:
            video_seek = str(video_description['data-player-seek'])
            title = video_description.text
            if content_index > 0:
                items[content_index][ITEM_URL] = items[content_index][ITEM_URL] + '&end=' + video_seek

            video_links_tag = content_detail.find('div',
                {'class': lambda attr_value: attr_value is not None
                     and attr_value.startswith('video_links')
                     and len(attr_value) >= len('video_links')})

            if video_links_tag is None:
                show_media = full_show_audio
            else:
                transcript_tag = video_links_tag.find('a', text=re.compile(r'Transcript'))
                show_video_page = transcript_tag['href'].split('#')[0]

                show_video_image_containers = html.findAll('a',
                   {'href': lambda attr_value: attr_value is not None
                       and attr_value.startswith(show_video_page)
                       and len(attr_value) >= len(show_video_page)})
                if len(show_video_image_containers) >= 2:
                    show_video_img = show_video_image_containers[1].find('img')
                    if show_video_img:
                        poster_url = show_video_img['src']


            media_url = show_media + '?start=' + video_seek

        content_index = content_index + 1

        items.append({
            ITEM_TITLE: title,
            ITEM_URL: media_url,
            ITEM_MEDIA_TYPE: 'video',
            ITEM_POSTER_URL: poster_url,
            ITEM_SUMMARY: summary
        })


    return [item for item in items if (item['url'] and item['media_type'])
            or item['title'] or item['summary']]

def get_shows():
    html = _html(_url('/shows'))
    # retrieve all the news item links
    shows_info = html.find('div',
        {'class': lambda attr_value: attr_value is not None
            and attr_value.startswith('recent_shows')
            and len(attr_value) >= len('recent_shows')})
    show_details = shows_info.findAll('div',
        {'class': lambda attr_value: attr_value is not None
          and attr_value.startswith('row heading')
          and len(attr_value) >= len('row heading')})

    shows = []

    for detail in show_details:
        show_title = detail.find('h5').text
        full_show_tag = detail.find('a', text=re.compile(r'Full Show'))
        show_path = full_show_tag['href']
        shows.append({
            'title': show_title,
            'url': _url(show_path)
        })
    shows[0]['title'] = 'Todays Show'
    return shows

def get_weekly_archive_links():
    html = _url('/shows')
    
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
    return get_show_videos(url)






