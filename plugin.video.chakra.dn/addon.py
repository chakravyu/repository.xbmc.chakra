import logging
import json
from xbmcswift2 import Plugin,Module,actions,xbmc,xbmcgui
from resources.lib.dn.api import DN

plugin = Plugin()

api = DN()

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

def clear_cache_ctx() :
    label = 'Clear Cache'
    cc_url = plugin.url_for('clear_cache')
    return (label, actions.background(cc_url))

@plugin.route('/context/clear_cache/')
def clear_cache() :
    plugin.clear_function_cache()


@plugin.route('/')
def index():
    #print 'Cache period : ' + str(get_cache_period())
    return get_root_paths()

def get_root_paths() :
    items = [{
        'label': 'Todays Shows',
        'path': plugin.url_for('show_todays_shows'),
        'context_menu' : [clear_cache_ctx()]
    }]
    return items

@plugin.route('/Todays Shows')
def show_todays_shows() :
    items = get_todays_show_items()
    return plugin.finish(items, update_listing=True)

def get_todays_show_items() :
    todays_shows = api.get_todays_shows()

    items = [{
        'label': todays_show.title,
        'path': plugin.url_for('show_todays_show_stream', url=todays_show.url),
        'info_type' : 'video',
        'info' : '',
        'context_menu' : [
                        ('Movie Information', 'XBMC.Action(Info)'),
                        clear_cache_ctx()
                        ],
        'icon' : todays_show.poster_url,
        'is_playable': True
    } for todays_show in todays_shows]
    return items

@plugin.route('/Todays Shows/<url>/')
def show_todays_show_stream(url):
    plugin.set_resolved_url(url)

if __name__ == '__main__':
    plugin.run()

