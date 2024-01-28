from model import artist, playlist, track
from model.spotify import spotify_user_playlists


test_artist_name = "YOASOBI"
test_artist_id = "some-random-id"
test_artist = artist.Artist(test_artist_name, test_artist_id)
test_track_name = "アイドル"
test_track_id = "some-track-td"
test_duration = 100
test_track = track.Track(test_track_name, test_track_id, test_duration, test_artist)
test_playlist_name = "Anime Now"
test_playlist_description = "An anime playlist"
test_playlist_id = "some-playlist-id"
test_playlist = playlist.Playlist(test_playlist_name, test_playlist_id, test_playlist_description)


def test_spotify_user_playlists():
    user_playlists = [test_playlist]
    liked_playlist = spotify_user_playlists.LikedSongsPlaylist()
    spotify_user_playlist = spotify_user_playlists.UserPlaylists(user_playlists, liked_playlist)
    assert spotify_user_playlist.user_playlists == user_playlists
    assert spotify_user_playlist.liked_songs_playlist == liked_playlist


def test_num_playlists_includes_liked_songs_count():
    user_playlists = []
    liked_playlist = spotify_user_playlists.LikedSongsPlaylist()
    spotify_user_playlist = spotify_user_playlists.UserPlaylists(user_playlists, liked_playlist)
    assert spotify_user_playlist.get_num_playlists() == 0 + 1

    user_playlists = [test_playlist]
    liked_playlist = spotify_user_playlists.LikedSongsPlaylist()
    spotify_user_playlist = spotify_user_playlists.UserPlaylists(user_playlists, liked_playlist)
    assert spotify_user_playlist.get_num_playlists() == 1 + 1


def test_user_playlists_builder():
    playlist_builder = spotify_user_playlists.UserPlaylistsBuilder()
    user_playlists = playlist_builder.build()
    assert user_playlists.get_num_playlists() == 1
    assert len(user_playlists.user_playlists) == 0
    assert user_playlists.liked_songs_playlist is not None


def test_user_playlists_builder_sets_liked_songs():
    playlist_builder = spotify_user_playlists.UserPlaylistsBuilder()
    liked_playlist = spotify_user_playlists.LikedSongsPlaylist()
    liked_playlist.add(test_track)
    playlist_builder.set_liked_songs(liked_playlist)
    user_playlists = playlist_builder.build()
    assert user_playlists.get_num_playlists() == 1
    assert user_playlists.liked_songs_playlist == liked_playlist
