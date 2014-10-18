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
    #plugin.clear_function_cache()
    return get_root_paths()

def get_root_paths() :
    weekly_archives = api.get_weekly_archives()
    items = [{
        'label': weekly_archive.title,
        'path': plugin.url_for('show_weekly_archive_stream', url=weekly_archive.url),
        'context_menu' : [clear_cache_ctx()]
    }for weekly_archive in weekly_archives]

    items.insert(0, {
            'label': 'Todays Shows',
            'path': plugin.url_for('show_todays_shows')
        })
    items.append({
            'label': 'Web Exclusives',
            'path': plugin.url_for('show_web_exclusives', page='1')
        })
    items.append({
            'label': 'Amy\'s Columns',
            'path': plugin.url_for('show_amys_columns', page='1')
        })
    
    return items


@plugin.route('/Todays Shows')
def show_todays_shows() :
    items = get_todays_show_items('')
    return plugin.finish(items)


def get_todays_show_items(url) :
    todays_shows = api.get_todays_shows(url)

    items = [{
        'label': todays_show.title,
        'path': plugin.url_for('show_todays_show_stream', url=todays_show.url),
        'info_type' : todays_show.media_type,
        'info' : {'plot': todays_show.summary, 'title' : todays_show.title},
        'context_menu' : [
                        ('Movie Information', 'XBMC.Action(Info)'),
                        clear_cache_ctx()
                        ],
        'icon' : todays_show.poster_url,
        'is_playable': True
    } for todays_show in todays_shows]
    return items

@plugin.cached(TTL=60*24*1)
@plugin.route('/Todays Shows/<url>/')
def show_todays_show_stream(url):
    plugin.set_resolved_url(url)


@plugin.route('/Weekly Archives')
def show_weekly_archives() :
    weekly_archives = api.get_weekly_archives()
    items = []
    for weekly_archive in weekly_archives :
        shows = show_weekly_archive_stream(weekly_archive.url)
        for show in shows:
            items.append(show)
    return items
    
@plugin.cached(TTL=60*24*7)
@plugin.route('/Weekly Archives/<url>')
def show_weekly_archive_stream(url) :
    items = get_todays_show_items(url)
    return plugin.finish(items)

@plugin.route('/Web Exclusives/<page>/')
def show_web_exclusives(page):
    return show_paged_shows('/categories/19?page=', page);

@plugin.route('/Amy\'s Column/<page>/')
def show_amys_columns(page):
    return show_paged_shows('/categories/11?page=', page);

@plugin.route('/<path>/<page>/')
def show_paged_shows(path, page):
    page = int(page)

    items = []

    items = get_todays_show_items(path + str(page))

    if len(items) == 0:
        next_page = False
    else:
        next_page = True

    if next_page:
        items.insert(0, {
            'label': 'Next >>',
            'path': plugin.url_for('show_paged_shows', path = str(path), page=str(page + 1))
        })

    if page > 1:
        items.insert(0, {
            'label': '<< Previous',
            'path': plugin.url_for('show_paged_shows', path = str(path), page=str(page - 1))
        })

    return plugin.finish(items)

if __name__ == '__main__':
    plugin.run()

