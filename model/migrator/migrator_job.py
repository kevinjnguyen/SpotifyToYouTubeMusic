from model.spotify import spotify_playlist


class Job(object):
    from_playlist: spotify_playlist.SpotifyPlaylist

    def __init__(self, from_playlist: spotify_playlist.SpotifyPlaylist):
        self.from_playlist = from_playlist
