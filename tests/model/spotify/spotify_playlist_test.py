from model.spotify import spotify_playlist


def test_liked_songs_playlist():
    liked_songs = spotify_playlist.LikedSongsPlaylist()
    assert liked_songs.name == "Liked Songs"
    assert liked_songs.id == "me"
    assert liked_songs.description == "Liked songs on Spotify"


def test_playlist():
    test_playlist_name = "Anime Now"
    test_playlist_description = "An anime playlist"
    test_playlist_id = "some-playlist-id"
    test_playlist = spotify_playlist.SpotifyPlaylist(test_playlist_name, test_playlist_id, test_playlist_description)
    assert test_playlist.name == test_playlist_name
    assert test_playlist.description == test_playlist_description
    assert test_playlist.id == test_playlist_id
