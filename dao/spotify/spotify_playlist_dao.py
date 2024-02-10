import time
from typing import Any, Dict, List
import spotipy

from dao.spotify.spotify_playlist_id import SpotifyPlaylistId
from dao.spotify.spotify_track import SpotifyTrack, SpotifyTrackId
from model import artist, track
from model.spotify import spotify_playlist

class SpotifyPlaylistDAO():

    def __init__(self, api: spotipy.Spotify, api_delay: float = 0.3):
        self.api = api
        self.api_delay = api_delay

    def get_playlist_count(self) -> int:
        current_user_playlists = self.api.current_user_playlists(limit=1)
        num_playlists = int(current_user_playlists["total"])
        return num_playlists
    
    def get_playlists(self, offset: int = 0, batch_size: int = 10) -> List[SpotifyPlaylistId]:
        playlist_ids: List[SpotifyPlaylistId] = []
        current_user_playlists = self.api.current_user_playlists(offset=offset, limit=batch_size)
        SpotifyPlaylistDAO.verifyFieldExists(current_user_playlists, 'items')
        for api_playlist in current_user_playlists['items']:
            SpotifyPlaylistDAO.verifyFieldExists(api_playlist, 'id')
            playlist_id = api_playlist['id']
            spotify_playlist_id = SpotifyPlaylistId(playlist_id)
            playlist_ids.append(spotify_playlist_id)
        return playlist_ids
    
    def get_all_playlists(self) -> List[SpotifyPlaylistId]:
        playlist_ids: List[SpotifyPlaylistId] = []
        next_batch = self.get_playlists()
        while len(next_batch) > 0:
            playlist_ids += next_batch
            time.sleep(self.api_delay)
            next_batch = self.get_playlists(offset=len(playlist_ids))    
        return playlist_ids
    
    def get_playlist(self, playlist_id: SpotifyPlaylistId) -> spotify_playlist.SpotifyPlaylist:
        api_playlist = self.api.playlist(playlist_id)
        SpotifyPlaylistDAO.verifyFieldExists('id')
        id = api_playlist['id']
        SpotifyPlaylistDAO.verifyFieldExists('name')
        name = api_playlist['name']
        SpotifyPlaylistDAO.verifyFieldExists('description')
        description = api_playlist['description']
        tracks = self.get_all_tracks(self, playlist_id)
        return spotify_playlist.SpotifyPlaylist(name, id, description, tracks)

    def get_liked_playlist(self, playlist_id: SpotifyPlaylistId) -> spotify_playlist.LikedSongsPlaylist:
        playlist_tracks: List[track.Track] = []
        next_batch = self.api.current_user_saved_tracks()
        SpotifyPlaylistDAO.verifyFieldExists(next_batch, 'items')
        while len(next_batch['items']) > 0:
            for api_track in next_batch['items']:
                spotify_track = SpotifyPlaylistDAO.parse_track(api_track)
                playlist_tracks.append(spotify_track)
            time.sleep(self.api_delay)
            next_batch = self.api.current_user_saved_tracks(playlist_id, offset=len(playlist_tracks))
        return spotify_playlist.LikedSongsPlaylist()

    def get_tracks(self, playlist_id: SpotifyPlaylistId, offset: int = 0, batch_size: int = 10) -> List[track.Track]:
        playlist_tracks: List[track.Track] = []
        current_playlist_tracks = self.api.playlist_tracks(playlist_id.id, offset=offset, limit=batch_size)
        SpotifyPlaylistDAO.verifyFieldExists(current_playlist_tracks, 'items')
        for api_track in current_playlist_tracks['items']:
            SpotifyPlaylistDAO.verifyFieldExists(api_track, 'track')
            spotify_track = SpotifyPlaylistDAO.parse_track(api_track['track'])
            playlist_tracks.append(spotify_track)
        return playlist_tracks
    
    def get_all_tracks(self, playlist_id: SpotifyPlaylistId) -> List[track.Track]:
        tracks: List[track.Track] = []
        next_batch = self.get_tracks(playlist_id)
        while len(next_batch) > 0:
            tracks += next_batch
            time.sleep(self.api_delay)
            next_batch = self.get_tracks(playlist_id, offset=len(tracks))
        return tracks
    
    def parse_track(api_track: Dict[str, Any]) -> SpotifyTrack:
        spotify_artist = SpotifyPlaylistDAO.parse_artist(api_track)
        SpotifyPlaylistDAO.verifyFieldExists(api_track, 'name')
        track_name = api_track['name']
        SpotifyPlaylistDAO.verifyFieldExists(api_track, 'id')
        track_id = SpotifyTrackId(api_track['id'])
        SpotifyPlaylistDAO.verifyFieldExists(api_track, 'duration_ms')
        duration_ms = int(api_track['duration_ms'])
        return SpotifyTrack(track_name, track_id, duration_ms, spotify_artist)
    
    def parse_artist(api_track: Dict[str, Any]) -> artist.Artist:
        SpotifyPlaylistDAO.verifyFieldExists(api_track, 'artists')
        api_track_artists = api_track['artists']
        if len(api_track_artists) < 1:
            raise SpotifyDAOException('invalid track: missing artists')
        head_artist = api_track_artists[0]
        SpotifyPlaylistDAO.verifyFieldExists(head_artist, 'name')
        SpotifyPlaylistDAO.verifyFieldExists(head_artist, 'id')
        return artist.Artist(head_artist['name'], head_artist['id'])

    def verifyFieldExists(api_response: Dict[str, Any], field_name: str) -> None:
        if api_response is None:
            raise SpotifyDAOException(f'invalid api response')
        
        if field_name not in api_response:
            raise SpotifyDAOException(f"missing field: '{field_name}' from API response")

class SpotifyDAOException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
