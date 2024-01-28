from typing import List
from model import playlist
from model.spotify.spotify_playlist import LikedSongsPlaylist


class UserPlaylists(object):
    def __init__(self, user_playlists: List[playlist.Playlist], liked_songs_playlist: LikedSongsPlaylist):
        self.user_playlists = user_playlists
        self.liked_songs_playlist = liked_songs_playlist

    def get_num_playlists(self) -> int:
        return len(self.user_playlists) + 1


class UserPlaylistsBuilder(object):

    playlists: List[playlist.Playlist]
    liked_songs_playlist: LikedSongsPlaylist

    def __init__(self):
        self.playlists = []
        self.liked_songs_playlist = LikedSongsPlaylist()

    def add_playlist(self, playlist: playlist.Playlist) -> None:
        self.playlists.append(playlist)

    def set_liked_songs(self, liked_songs_playlist: LikedSongsPlaylist) -> None:
        self.liked_songs_playlist = liked_songs_playlist

    def build(self) -> UserPlaylists:
        return UserPlaylists(self.playlists, self.liked_songs_playlist)
