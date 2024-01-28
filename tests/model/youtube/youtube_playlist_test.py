from model.youtube import youtube_playlist


def test_playlist():
    test_playlist_name = "Anime Now"
    test_playlist_description = "An anime playlist"
    test_playlist_id = "some-playlist-id"
    test_playlist = youtube_playlist.YouTubePlaylist(test_playlist_name, test_playlist_id, test_playlist_description)
    assert test_playlist.name == test_playlist_name
    assert test_playlist.description == test_playlist_description
    assert test_playlist.id == test_playlist_id
