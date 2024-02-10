from dataclasses import dataclass


@dataclass
class SpotifyPlaylistId:
    def __init__(self, id: str):
        self.id = id
