from dataclasses import dataclass


@dataclass(frozen=True)
class SpotifyPlaylistId:
    id: str
