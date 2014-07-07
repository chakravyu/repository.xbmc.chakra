import logging
import json
from xbmcswift2 import Plugin,Module,actions,xbmc,xbmcgui
from resources.lib.nfdc.api import NFDC

plugin = Plugin()

api = NFDC()

def get_cache_period() :

    choice = plugin.get_setting('cache_period', int);
    if choice == 0 :
        return 0
    elif choice == 1 :
        return 1
    elif choice == 2 :
        return 7
    elif choice == 3 :
        return 30
    elif choice == 4 :
        return 365

    return 0


# for contect menu 'Movie Information'
# context menu : 'Movie Information', 'XBMC.Action(Info)'
#
# http://mirrors.xbmc.org/docs/python-docs/stable/xbmcgui.html#ListItem
# items = 'info_type' : 'video', 'info' : {'title': video['name'], 'year': int(video['year']), 'type': 'movie', 'plotoutline': description, 'plot': description, 'mpaa': mpaa})

@plugin.route('/')
def index():
    #print 'Cache period : ' + str(get_cache_period())
    return get_root_paths()

@plugin.cached(TTL=60*24*365)
def get_root_paths() :
    items = [{
        'label': 'movies',
        'path': plugin.url_for('show_movies',page='1'),
        'context_menu' : [clear_cache_ctx()]
    }]
    return items

@plugin.route('/movies/<page>')
def show_movies(page):

    page = int(page)

    max_page = get_max_page()

    if page == max_page:
        next_page = False
    else:
        next_page = True

    items = get_movie_items(page)

    sorted_items = sorted(items, key=lambda item: item['label'])

    if next_page:
        sorted_items.insert(0, {
            'label': 'Next >>',
            'path': plugin.url_for('show_movies', page=str(page + 1))
        })

    if page > 1:
        sorted_items.insert(0, {
            'label': '<< Previous',
            'path': plugin.url_for('show_movies', page=str(page - 1))
        })

    return plugin.finish(sorted_items, update_listing=True)

def clear_cache_ctx() :
    label = 'Clear Cache'
    cc_url = plugin.url_for('clear_cache')
    return (label, actions.background(cc_url))

def get_movies(page) :
    return api.get_movies(page)

def get_movie_info(url) :
    movie = get_movie_data(url)
    return movie['info']

@plugin.route('/context/clear_cache/')
def clear_cache() :
    plugin.clear_function_cache()

@plugin.route('/movies/<page>/<url>/')
def show_movie_stream(page,url):
    movie = get_movie_data(url)
    plugin.set_resolved_url(movie['url'], movie['sub_url'])


## Cached methods
@plugin.cached(TTL=get_cache_period()*60*24)
def get_movie_items(page) :

    page = int(page)

    movies = get_movies(page)

    items = [{
        'label': movie.name,
        'path': plugin.url_for('show_movie_stream', page=page,url=movie.url),
        'info_type' : 'video',
        'info' : get_movie_info(movie.url),
        'context_menu' : [
                        ('Movie Information', 'XBMC.Action(Info)'),
                        clear_cache_ctx()
                        ],
        'icon' : movie.img_path,
        'is_playable': True
    } for movie in movies]
    return items


@plugin.cached(TTL=get_cache_period()*60*24)
def get_max_page() :
    api = NFDC()
    return api.get_max_page()

@plugin.cached(TTL=60*24*365)
def get_movie_data(url) :
    return api.get_movie_data(url)


if __name__ == '__main__':
    plugin.run()
