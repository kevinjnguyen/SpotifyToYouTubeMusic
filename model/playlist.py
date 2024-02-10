from typing import List
from model import track


class Playlist(object):
    def __init__(self, name: str, id: str, description: str, tracks: List[track.Track]):
        self.name = name
        self.id = id
        self.description = description
        self.tracks: List[track.Track] = tracks

    def num_tracks(self) -> int:
        return len(self.tracks)

    def __str__(self) -> str:
        return f"Playlist - Name: {self.name}, ID: {self.id}, Description: {self.description}, Tracks: {self.tracks}"

    def __repr__(self) -> str:
        return f"Playlist({self.name}, {self.id}, {self.description}, {self.tracks})"

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, Playlist):
            return (
                self.name == other.name
                and self.id == other.id
                and self.description == other.description
                and set(self.tracks) == set(other.tracks)
            )
        return False

class FailedPlaylist(Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description)


class InvalidPlaylistException(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"missing field: {field_name}")
