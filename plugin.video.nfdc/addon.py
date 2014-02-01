
import json
from xbmcswift2 import Plugin,Module,xbmc,xbmcgui
from resources.lib.nfdc.api import NFDC

plugin = Plugin()

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


@plugin.route('/')
def index():
    items = [
        {'label': 'movies', 'path': plugin.url_for('show_movies',page='1')}
    ]
    print 'Cache period : ' + str(get_cache_period())
    return items



@plugin.route('/movies/<page>')
def show_movies(page):
      
    page = int(page)
    
    movies = get_movies(page)    
    max_page = get_max_page()
    
    if page == max_page:
        next_page = False
    else:
        next_page = True

    items = [{
        'label': movie.name,
        'path': plugin.url_for('show_movie_stream', page=page,url=movie.url),
        'is_playable': True
    } for movie in movies]

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

@plugin.route('/movies/<page>/<url>/')
def show_movie_stream(page,url):    
    stream = get_movie_stream(url)
    plugin.set_resolved_url(stream['url'], stream['sub_url'])
            
## Cached methods            
@plugin.cached(TTL=get_cache_period()*60*24)
def get_movies(page) :
    api = NFDC()
    return api.get_movies(page)

@plugin.cached(TTL=get_cache_period()*60*24)
def get_max_page() :
    api = NFDC()
    return api.get_max_page()

@plugin.cached(TTL=get_cache_period()*60*24)
def get_movie_stream(url) :
    api = NFDC()
    return api.get_movie_stream(url)



if __name__ == '__main__':
    plugin.run()
