from dataclasses import dataclass
from enum import Enum
import logging
from typing import Dict
from adaptor import local_storage
from dao.spotify.spotify_playlist_id import SpotifyPlaylistId
from model import playlist
from model.spotify.spotify_playlist import SpotifyPlaylist

logger = logging.getLogger(__name__)


class MigratorState(Enum):
    NONE = 1
    POPULATED = 2


@dataclass
class MigratorStateful:
    playlists: Dict[SpotifyPlaylistId, SpotifyPlaylist]
    state: MigratorState

    def __init__(self, 
                 playlists={}, 
                 state=MigratorState.NONE, 
                 already_processed = set(),
                 failed = set()):
        self.playlists = playlists
        self.state = state
        self.already_processed = already_processed
        self.failed = failed


class MigratorData(local_storage.LocalSerializable):
    def __init__(self, local_file_name: str):
        super().__init__(local_file_name)
        if self.data is None:
            logger.info("No previous migrator data saved.")
            self.data = MigratorStateful()

    def add_playlist(self, playlist: playlist.Playlist) -> None:
        if self.contains_playlist(playlist):
            raise AlreadyProcessedException(playlist)
        self.data.playlists[playlist.id] = playlist

    def remove_playlist(self, playlist: playlist.Playlist) -> None:
        if not self.contains_playlist(playlist):
            raise NoSuchPlaylistException(playlist)
        del self.data.playlists[playlist.id]

    def contains_playlist(self, playlist: playlist.Playlist) -> bool:
        return playlist.id in self.data.playlists

    def get_state(self) -> MigratorState:
        return self.data.state

    def set_populated(self) -> None:
        self.data.state = MigratorState.POPULATED

    def success(self, playlistId: str) -> None:
        self.data.already_processed.add(playlistId)

    def failure(self, playlistId: str) -> None:
        self.data.failed.add(playlistId)

    def __eq__(self, other) -> bool:
        if isinstance(other, MigratorData):
            if self.data.state == other.data.state:
                if len(self.data.playlists) == len(other.data.playlists):
                    for id, playlist in self.data.playlists.items():
                        if not other.data[id] == playlist:
                            return False
                    return True
        return False


class AlreadyProcessedException(Exception):
    def __init__(self, playlist: playlist.Playlist):
        super().__init__(f"already processed: {playlist}")
        self.playlist = playlist


class NoSuchPlaylistException(Exception):
    def __init__(self, playlist: playlist.Playlist):
        super().__init__(f"no such playlist: {playlist}")
