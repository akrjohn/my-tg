# -*- coding: utf-8 -*-
# Module: default
# Author: Roman V. M.
# Created on: 28.11.2014
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import json
import jmodule

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

# Free sample videos are provided by www.vidsplay.com
# Here we use a fixed set of properties simply for demonstrating purposes
# In a "real life" plugin you will need to get info and links to video files/streams
# from some web-site or online service.

def displayMovies():
  js = json.load(open("C:\\Users\\John\\AppData\\Roaming\\Kodi\\addons\\plugin.video.TamilGun\\allmovies1.json"))
  #xbmcgui.Dialog().ok("Hello", "John", "said", "so")
  for k,v in js.items():
    if k=='rows':
      for row in v:
        for k1,v1 in row.items():
          if k1=='key':
            list_item = xbmcgui.ListItem(label='dummy')
            url=''
            mname=''
            mimage=''
            mvideo=''

            for k2,v2 in v1.items():
              if k2=='movie':
                # Create a list item with a text label and a thumbnail image.
                mname=unicode(v2).encode('utf-8')
                list_item.setLabel(mname)
                list_item.setInfo('video', {'title': v2, 'genre': 'Tamil'})
                              #print('Movie name :'+v2)
              elif k2=='image':
                mimage=unicode(v2).encode('utf-8')
                list_item.setArt({'thumb': v2, 'icon': v2, 'fanart': v2})
                #print('Movie image :'+v2)
              elif k2=='videoLink':
                  url = get_url(action='listMovies', videoLink=v2, title=mname, image=mimage)
                  #print('Movie Link :'+video)
            list_item.setProperty('IsPlayable', 'false')
            is_folder = True
            xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
  xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_PLAYLIST_ORDER)
  # Finish creating a virtual folder.
  xbmcplugin.endOfDirectory(_handle)

def displayMovieLinks(moviePath, movieName, movieImage):
  movieLinks = jmodule.getMoviesInIframe(moviePath)
  for movie in movieLinks:
    list_item = xbmcgui.ListItem(label=movieName)
    list_item.setInfo('video', {'title': movieName, 'genre': 'Tamil'})
    list_item.setArt({'thumb': movieImage, 'icon': movieImage, 'fanart': movieImage})
    url = get_url(action='play', video=movie)
    list_item.setProperty('IsPlayable', 'true')
    is_folder = False
    xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
  xbmcplugin.endOfDirectory(_handle)

def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def play_video(path):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.
    play_item = xbmcgui.ListItem(path=path)
    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    #params = dict(parse_qsl(paramstring,encoding='utf-8'))
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'listing':
            # Display the list of videos in a provided category.
            list_videos(params['category'])
        elif params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['video'])
        elif params['action'] == 'listMovies':
            displayMovieLinks(params['videoLink'], params['title'], params['image'])
        else :
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        #list_categories()
        displayMovies()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])