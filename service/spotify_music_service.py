from dataclasses import dataclass
import logging
from typing import List, Optional
from dao.spotify.spotify_playlist_dao import SpotifyPlaylistDAO

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from model.spotify import spotify_playlist


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CurrentUserPlaylists:
    playlists: List[spotify_playlist.SpotifyPlaylist]


@dataclass(frozen=True)
class SpotifyMusicServiceException(Exception):
    e: Exception


class SpotifyMusicService:

    def __init__(self, spotify_playlist_dao: Optional[SpotifyPlaylistDAO] = None):
        if spotify_playlist_dao is None:
            self.dao = SpotifyPlaylistDAO(self.__get_spotify_api())
        else:
            self.dao = spotify_playlist_dao

    def __get_spotify_api(
        self, auth_scope="playlist-read-private,playlist-read-collaborative,user-library-read"
    ) -> spotipy.Spotify:
        logger.info(f"Initializing Spotify API with scope: {auth_scope}")
        return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=auth_scope))

    def get_current_user_playlists(
        self, include_liked_songs: bool = True, ignore_failures: bool = True
    ) -> CurrentUserPlaylists:
        all_playlist_ids = self.dao.get_all_playlists()
        logger.info(f"Retrieved: {len(all_playlist_ids)} playlists.")
        all_playlists: List[spotify_playlist.SpotifyPlaylist] = []
        for playlist_id in all_playlist_ids:
            child_logger = logger.getChild(playlist_id.id)
            try:
                all_playlists.append(self.dao.get_playlist(playlist_id, logger=child_logger))
            except Exception as e:
                if ignore_failures:
                    child_logger.error(f"Failed to process playlist ID: {playlist_id}: {e}")
                else:
                    raise SpotifyMusicServiceException(e)
                
            if len(all_playlists) % 10 == 0:
                logger.info(f'Successfully fetched: {len(all_playlists)} / {len(all_playlist_ids)}')

        logger.info(f'Completed playlist retrieval: {len(all_playlists)} total for migration.')

        try:
            if include_liked_songs:
                liked_playlist = self.dao.get_liked_playlist()
                all_playlists.append(liked_playlist)
        except Exception as e:
            if ignore_failures:
                logger.error(f"Failed to process liked playlist: {e}")
            else:
                raise SpotifyMusicServiceException(e)

        return CurrentUserPlaylists(all_playlists)
