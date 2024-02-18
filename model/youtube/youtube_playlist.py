from dataclasses import dataclass
from model import playlist


@dataclass
class YoutubePlaylistId:
    id: str


class YoutubePlaylist(playlist.Playlist):
    def __init__(self, name: str, id: YoutubePlaylistId, description: str):
        super().__init__(name, id.id, description, [])
