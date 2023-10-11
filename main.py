from gui import GUI
from api import API

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from dotenv import dotenv_values

config = dotenv_values()

scope = 'playlist-modify-public playlist-modify-private user-library-read user-modify-playback-state'
spot = Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=config['SPOTIFY_ID'], client_secret=config['SPOTIFY_SECRET'], redirect_uri=config['SPOTIFY_URI']))

gui = GUI(API(spot))
# TODO load json if exists

gui.start()
