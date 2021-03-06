#!/usr/bin/env python

from scaffold import *
from spotify import authenticate
from spotify import fetch_saved_tracks
from spotify import save_songs_to_file
from spotify import download_songs
from youtube import fetch_youtube_url
import spotipy
import argparse

if __name__ == '__main__':
    log.info('Starting spotify-dl')

    parser = argparse.ArgumentParser(prog='spotify-dl')
    parser.add_argument('-d', '--download', action='store_true', help='Download using youtube-dl')
    parser.add_argument('-V', '--verbose', action='store_true', help='Show more information on what''s happening.')
    parser.add_argument('-o' , '--output',type=str,action='store',nargs='*',help='Specify download diretory.')
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)

    token = authenticate()
    if args.output:
        download_directory = args.output[0]
            #Check whether directory has a trailing slash or not
        if len(download_directory) >=0 and download_directory[-1] != '/':
            download_directory+='/'
    else:
        download_directory=''
    


    sp = spotipy.Spotify(auth=token)
    songs = fetch_saved_tracks(sp)
    url = []
    for s in songs:
        link = fetch_youtube_url(s)
        if link:
            url.append(link)
    save_songs_to_file(url)
    if args.download == True:
        download_songs(url,download_directory)
