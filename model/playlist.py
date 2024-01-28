from typing import List
from model import track


class Playlist(object):
    def __init__(self, name: str, id: str, description: str):
        self.name = name
        self.id = id
        self.description = description
        self.tracks: List[track.Track] = []

    def add(self, track: track.Track) -> None:
        self.tracks.append(track)

    def size(self) -> int:
        return len(self.tracks)

    def __str__(self) -> str:
        return f"Playlist - Name: {self.name}, ID: {self.id}, Description: {self.description}, Tracks: {self.tracks}"

    def __repr__(self) -> str:
        return f"Playlist({self.name}, {self.id}, {self.description}, {self.tracks})"
