from model import playlist


class LikedSongsPlaylist(playlist.Playlist):
    def __init__(self):
        super().__init__("Liked Songs", "me", "Liked songs on Spotify")
