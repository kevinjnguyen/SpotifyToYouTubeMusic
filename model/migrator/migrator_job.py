from model.spotify import spotify_playlist
from model.youtube import youtube_playlist


class Job(object):
    from_playlist: spotify_playlist.SpotifyPlaylist

    def __init__(self, from_playlist: spotify_playlist.SpotifyPlaylist, to_playlist: youtube_playlist.YouTubePlaylist):
        self.from_playlist = from_playlist
        self.to_playlist = to_playlist
        self.current_track_index = 0

    def successful(self) -> None:
        self.current_track_index += 1

    def is_complete(self) -> bool:
        return len(self.from_playlist.tracks) == self.current_track_index
