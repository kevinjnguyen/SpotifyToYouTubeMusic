from model import playlist


class YouTubePlaylist(playlist.Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description)
