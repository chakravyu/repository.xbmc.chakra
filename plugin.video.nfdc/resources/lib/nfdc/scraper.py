'''
    nfdc.scraper
    ~~~~~~~~~~~~~~~~~~~~~

    This module contains some functions which do the website scraping for the
    API module. You shouldn't have to use this module directly.
'''
import re,json,os
from urllib2 import urlopen
from urlparse import urljoin
from BeautifulSoup import BeautifulSoup as BS

max_page = 0


BASE_URL = 'http://www.cinemasofindia.com/browse/movies'
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


def get_movies(page):
    '''Returns a list of movies. Each movie is a dict with
    keys of 'name' and 'url'.
    '''
    url = _url('?page=' + str(page))
    html = _html(url)
    subjs = html.findAll('a',
        {'href': lambda attr_value: attr_value.startswith('/movie/view/')
                                    and len(attr_value) > len('/movie/view/')})

    items = []
    
    urls = set()
    for subj in subjs:
        url = _url(subj['href'])
        if url not in urls:
            urls.add(url)
            items.append({
                'name': subj['href'].split('_')[1],
                'url': url,
            })

    return [item for item in items if item['name'] and item['url']]

def get_max_page():
    global max_page
    if max_page == 0 :
        url = _url('?page=1')
        html = _html(url)
        pagejs = html.findAll('a',
            {'href': lambda attr_value: attr_value.startswith(BASE_URL + '?page=')
                                        and len(attr_value) > len(BASE_URL + '?page=')})
        pages = []
    
        for page in pagejs:                                    
            pages.append(int(page['href'].split('=')[1]))
        max_page = max(pages)
    return max_page

def get_movie_stream(url):
    html = _html(url)
    scriptjs = html.findAll('script',
        {'type': lambda attr_value: attr_value == 'text/javascript'})
    

    stream = {}
    
    for script in scriptjs:
        # get the movie stream (.m3u8 format) url
        regex_stream = re.compile(r'http.*\.m3u8')
        stream_url_match = regex_stream.search(str(script.string))

        # get the subtitles file (.srt) url
        regex_sub = re.compile(r'http.*\.srt\"')
        sub_url_match = regex_sub.search(str(script.string))

        if stream_url_match:  

            name = url.split('_')[1]
            sub_url = ''
            if sub_url_match:
                sub_url = sub_url_match.group()[:-1]         

            stream = {
                    'name': name,
                    'url': stream_url_match.group(),
                    'sub_url': sub_url
            }
            break

    return stream

