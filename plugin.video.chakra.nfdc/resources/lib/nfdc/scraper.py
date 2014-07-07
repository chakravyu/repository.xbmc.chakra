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

def get_title(url) :
    return url.split('_')[1]

def get_movies(page):
    '''Returns a list of movies. Each movie is a dict with
    keys of 'name' and 'url'.
    '''

    url = _url('?page=' + str(page))
    logging.info("movies page : " + url)
    html = _html(url)
    subjs = html.findAll('a',
        {'href': lambda attr_value: attr_value.startswith('/movie/view/')
                                    and len(attr_value) > len('/movie/view/')})

    items = []

    urls = set()
    for subj in subjs:
        url = _url(subj['href'])
        img = subj.find("img")
        img_path = ''
        logging.info("movie : " + url)
        if img :
            img_path = img['src']
            logging.info("img_path :" + img_path)
        if url not in urls:
            urls.add(url)
            items.append({
                'name': get_title(subj['href']),
                'url': url,
                'img_path' : img_path
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


def get_movie_info(html,title,has_subs):
    video_info = html.find("div", {"class":"video_info"})

    plot = ''
    cast = []
    director = ''
    genre = ''

    info = {}
    if video_info :
        plot_tag = video_info.find("p")
        if plot_tag :
            plot = plot_tag.text
            logging.info("plot : " + plot.encode('utf-8'))

        cast_tags = video_info.findAll("a",
                    {'href': lambda attr_value: attr_value.startswith("/actor/view")})
        for actor_tag in cast_tags :
            actor = actor_tag.text
            cast.append(actor)

        director_tag = video_info.find("a",
                    {'href': lambda attr_value: attr_value.startswith("/director/view")})
        if director_tag :
            director = director_tag.text
            logging.info("director : " + director)

        genre_tags = video_info.findAll("a",
                    {'href': lambda attr_value: attr_value.startswith("/browse/index?genre=")})
        for genre_tag in genre_tags :
            genre += (genre_tag.text + ' / ')
        genre = genre[:-2]
        logging.info("genre : " + genre)


        if has_subs :
            title += '  [English subtitles]'
            logging.info("title : " + title)
        info = {
                'plot' : plot,
                'cast' : cast,
                'director' : director,
                'genre' : genre,
                'title' : title
                }
    return info

def get_movie_data(url):
    html = _html(url)
    video_player_tag = html.find("div", {"id":"video_player"})


    movie_data = {}
    logging.info("url : " + url)
    if video_player_tag :
        # get the movie stream (.m3u8 format) url
        regex_stream = re.compile(r'http.*\.(m3u8|mp4)')
        #print "video_player_tag : " , video_player_tag.text
        stream_url_match = regex_stream.search(str(video_player_tag.text))
        stream_url = urllib.unquote(stream_url_match.group())
        logging.info("stream_url : " + stream_url)
        # get the subtitles file (.srt) url
        regex_sub = re.compile(r'http.*\.srt\"')
        sub_url_match = regex_sub.search(str(video_player_tag.text))

        if stream_url_match:

            name = url.split('_')[1]
            logging.info("name : " + name)
            sub_url = ''
            has_subs = False
            if sub_url_match:
                sub_url = sub_url_match.group()[:-1]
                has_subs = True
                logging.info("srt : " + sub_url)

            movie_data = {
                    'name': name,
                    'url': stream_url,
                    'sub_url': sub_url,
                    'info' : get_movie_info(html,get_title(url),has_subs)
            }


    return movie_data




