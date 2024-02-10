from dataclasses import dataclass
from typing import List
from dao.spotify.spotify_playlist_id import SpotifyPlaylistId
from model import playlist, track


@dataclass(frozen=True)
class SpotifyPlaylist(playlist.Playlist):
    name: str
    id: SpotifyPlaylistId
    description: str
    tracks: List[track.Track]

    def __init__(self, name: str, id: SpotifyPlaylistId, description: str, tracks: List[track.Track]):
        super().__init__(name, id.id, description, tracks)


@dataclass(frozen=True)
class LikedSongsPlaylist(SpotifyPlaylist):
    def __init__(
        self,
        name: str = "Liked Songs",
        id: SpotifyPlaylistId = SpotifyPlaylistId("api_liked_songs"),
        description: str = "Liked songs on Spotify",
        tracks: List[track.Track] = [],
    ):
        super().__init__(name, id, description, tracks)
