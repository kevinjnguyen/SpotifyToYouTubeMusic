from dataclasses import dataclass
from model import artist, track

@dataclass

class SpotifyTrackId:
    id: str

class SpotifyTrack(track.Track):
    def __init__(self, name: str, id: SpotifyTrackId, duration_ms: int, artist: artist.Artist):
        super().__init__(name, id, duration_ms, artist)
