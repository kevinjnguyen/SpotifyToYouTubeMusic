from typing import Any, Dict, List, Self
from dao.spotify.spotify_playlist_id import SpotifyPlaylistId
from model import playlist, track


class SpotifyPlaylist(playlist.Playlist):
    def __init__(self, name: str, id: SpotifyPlaylistId, description: str, tracks: List[track.Track]):
        super().__init__(name, id.id, description, tracks)

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        # TODO: Check tracks
        if isinstance(other, SpotifyPlaylist):
            return self.name == other.name and self.id == other.id and self.description == other.description
        return False


class LikedSongsPlaylist(SpotifyPlaylist):
    def __init__(
        self,
        name: str = "Liked Songs",
        id: SpotifyPlaylistId = SpotifyPlaylistId("api_liked_songs"),
        description: str = "Liked songs on Spotify",
        tracks: List[track.Track] = [],
    ):
        super().__init__(name, id, description, tracks)

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        # TODO: Check tracks
        if isinstance(other, LikedSongsPlaylist):
            return self.name == other.name and self.id == other.id and self.description == other.description
        return False
