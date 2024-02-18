from model import playlist


class YoutubePlaylist(playlist.Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description, [])
