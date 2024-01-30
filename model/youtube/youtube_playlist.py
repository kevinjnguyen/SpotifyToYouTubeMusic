from model import playlist


class YouTubePlaylist(playlist.Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description)

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, YouTubePlaylist):
            return self.name == other.name and self.id == other.id and self.description == other.description
        return False
