from model import playlist


class SpotifyPlaylist(playlist.Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description)

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, SpotifyPlaylist):
            return self.name == other.name and self.id == other.id and self.description == other.description
        return False


class LikedSongsPlaylist(SpotifyPlaylist):
    def __init__(self):
        super().__init__("Liked Songs", "me", "Liked songs on Spotify")

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, LikedSongsPlaylist):
            return self.name == other.name and self.id == other.id and self.description == other.description
        return False
