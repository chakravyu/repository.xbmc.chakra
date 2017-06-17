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

ITEM_URL = 'url'
ITEM_TITLE = 'title'
ITEM_MEDIA_TYPE = 'media_type'
ITEM_POSTER_URL = 'poster_url'
ITEM_SUMMARY = 'summary'

max_page = 0
shows_cache = {}

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
    html = _html(show_date_url)

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

            global shows_cache
            if video_links_tag is None:
                show_media = full_show_audio
            else:
                transcript_tag = video_links_tag.find('a', text=re.compile(r'Transcript'))
                show_video_page = transcript_tag['href'].split('#')[0]
                poster_url = shows_cache.get(show_video_page, full_show_img)
                # poster_url = shows_cache.get(show_video_page, "https://www.democracynow.org/images/story/13/37013/w320/S09_Kushner.jpg")

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


    # build shows cache

    shows_info_row = shows_info.findAll('div',
        {'class': lambda attr_value: attr_value is not None
            and attr_value.startswith('story')
            and len(attr_value) >= len('story')})

    global shows_cache
    for show_info in shows_info_row:
        show_story = show_info.find('a',
                {'data-ga-action': lambda attr_value: attr_value is not None})
        show_url = show_story['href']
        show_img = show_story.find('img')
        show_img_url = show_img['src']
        shows_cache[show_url] = show_img_url


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


def get_web_exclusive_media(url):
    html = _html(url)
    media_type = ''
    media_url = ''

    we_story_media = json.loads(unicode(html.find(id="story_video").contents[0].contents[0]))
    we_media_video_url = str(we_story_media['high_res_video'])

    if we_media_video_url:
        media_type = 'video'
        media_url = we_media_video_url
    else:
        we_media_audio_url = str(we_story_media['audio'])
        if we_media_audio_url:
            media_type = 'audio'
            media_url = we_media_audio_url

    return {
        'type': media_type,
        'url': media_url
    }


def get_web_exclusives(page):
    '''Returns a list of web exclusive videos. 
    '''
    url = _html(_url('/categories/web_exclusive'))

    return






