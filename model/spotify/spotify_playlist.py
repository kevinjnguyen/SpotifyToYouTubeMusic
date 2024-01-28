from model import playlist


class SpotifyPlaylist(playlist.Playlist):
    def __init__(self, name: str, id: str, description: str):
        super().__init__(name, id, description)


class LikedSongsPlaylist(SpotifyPlaylist):
    def __init__(self):
        super().__init__("Liked Songs", "me", "Liked songs on Spotify")
