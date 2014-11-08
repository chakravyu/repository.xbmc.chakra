#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh
workon xbmcswift2

xbmcswift2 run "plugin://plugin.video.chakra.dn/context/clear_cache/"
xbmcswift2 run "plugin://plugin.video.chakra.dn/"
xbmcswift2 run "plugin://plugin.video.chakra.dn/Todays Shows"
