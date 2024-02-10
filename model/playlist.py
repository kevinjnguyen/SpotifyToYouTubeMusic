from dataclasses import dataclass
from typing import List
from model import track


@dataclass(frozen=True)
class Playlist(object):
    name: str
    id: str
    description: str
    tracks: List[track.Track]


@dataclass(frozen=True)
class FailedPlaylist(Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description, [])


@dataclass(frozen=True)
class InvalidPlaylistException(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"missing field: {field_name}")
