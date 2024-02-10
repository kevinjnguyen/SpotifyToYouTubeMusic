from typing import Any, Dict
from model import artist, track

class SpotifyTrackId():
    def __init__(self, id: str):
        self.id = id

class SpotifyTrack(track.Track):    
    def __init__(self, name: str, id: SpotifyTrackId, duration_ms: int, artist: artist.Artist):
        super().__init__(name, id, duration_ms, artist)
