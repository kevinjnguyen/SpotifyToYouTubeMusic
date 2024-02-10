import logging
from dao.spotify.spotify_playlist_dao import SpotifyPlaylistDAO

import spotipy
from spotipy.oauth2 import SpotifyOAuth


logger = logging.getLogger(__name__)


class SpotifyMusicService(object):
    scope = "playlist-read-private,playlist-read-collaborative,user-library-read"

    def __init__(self, auth_scope: str = scope, api_delay: int = 0.3):
        super().__init__()
        logger.info("Initializing Spotify")
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=auth_scope))
        self.api_delay = api_delay
        logger.info(f"Successfully initialized Spotify. Scope: {auth_scope}, API Delay: {api_delay} seconds")
        self.dao = SpotifyPlaylistDAO(self.sp, self.api_delay)
