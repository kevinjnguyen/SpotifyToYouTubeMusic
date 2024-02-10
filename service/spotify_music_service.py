import logging
import time
import traceback
from typing import Dict, List, Set
from dao.spotify import spotify_track
from dao.spotify.spotify_playlist_dao import SpotifyPlaylistDAO
from model import playlist, track
from model.spotify import spotify_playlist

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

    def get_playlists_count(self) -> int:
        current_user_playlists = self.sp.current_user_playlists(limit=1)
        num_playlists = int(current_user_playlists["total"])
        return num_playlists

    def get_playlists(self, initial_offset: int = 0, batch_size: int = 10) -> List[spotify_playlist.SpotifyPlaylist]:
        playlists: List[spotify_playlist.SpotifyPlaylist] = []
        current_user_playlists = self.sp.current_user_playlists(offset=initial_offset, limit=batch_size)
        num_playlists = int(current_user_playlists["total"])
        if len(current_user_playlists["items"]) > 0:
            for current_playlist in current_user_playlists["items"]:
                playlist_id = current_playlist["id"]
                playlist_name = current_playlist["name"]
                try:
                    sp = self.process_playlist(current_playlist)
                    playlists.append(sp)
                    logger.info(
                        f"Processed: {len(playlists) + initial_offset} / {num_playlists}: {sp.name} with {len(sp.tracks)} tracks."
                    )
                except Exception as e:
                    raise PlaylistProcessingException(playlist_name, playlist_id, e)
        return playlists

    def get_liked_playlist(self) -> spotify_playlist.LikedSongsPlaylist:
        liked_playlist = spotify_playlist.LikedSongsPlaylist()
        current_liked_tracks = self.sp.current_user_saved_tracks()
        num_tracks = int(current_liked_tracks["total"])
        while current_liked_tracks:
            if len(current_liked_tracks["items"]) == 0 or num_tracks == len(liked_playlist.tracks):
                break
            for t in current_liked_tracks["items"]:
                liked_playlist.add(spotify_track.SpotifyTrack(t))
            time.sleep(self.api_delay)
            current_liked_tracks = self.sp.current_user_saved_tracks(offset=len(liked_playlist.tracks))
        return liked_playlist

    def process_playlist(self, p: Dict) -> spotify_playlist.SpotifyPlaylist:
        sp = spotify_playlist.get_playlist(p)
        sp_tracks = self.get_playlist_tracks(sp)
        sp.add_tracks(sp_tracks)
        return sp

    def get_playlist_tracks(self, target_playlist: spotify_playlist.SpotifyPlaylist) -> List[track.Track]:
        playlist_tracks: List[track.Track] = []
        current_playlist_tracks = self.sp.playlist_tracks(target_playlist.id)
        num_tracks = int(current_playlist_tracks["total"])
        while current_playlist_tracks:
            if len(current_playlist_tracks["items"]) == 0 or num_tracks == len(playlist_tracks):
                break
            for t in current_playlist_tracks["items"]:
                playlist_tracks.append(spotify_track.SpotifyTrack(t))
            time.sleep(self.api_delay)
            current_playlist_tracks = self.sp.playlist_tracks(target_playlist.id, offset=len(playlist_tracks))
        return playlist_tracks


class PlaylistProcessingException(Exception):
    def __init__(self, playlist_name: str, playlist_id: str, e: Exception):
        super().__init__(e)
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
