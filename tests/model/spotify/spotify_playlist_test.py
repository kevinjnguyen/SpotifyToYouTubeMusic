from model.spotify import spotify_playlist


def test_liked_songs_playlist():
    liked_songs = spotify_playlist.LikedSongsPlaylist()
    assert liked_songs.name == "Liked Songs"
    assert liked_songs.id == "me"
    assert liked_songs.description == "Liked songs on Spotify"
