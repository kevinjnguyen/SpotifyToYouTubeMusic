from model import artist, playlist, track


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


def test_playlist_str():
    test_playlist = playlist.Playlist(test_playlist_name, test_playlist_id, test_playlist_description)
    expected = "Playlist - Name: Anime Now, ID: some-playlist-id, Description: An anime playlist, Tracks: []"
    assert str(test_playlist) == expected


def test_playlist_add_str():
    test_playlist = playlist.Playlist(test_playlist_name, test_playlist_id, test_playlist_description)
    test_playlist.add(test_track)
    expected = "Playlist - Name: Anime Now, ID: some-playlist-id, Description: An anime playlist, Tracks: [Track('アイドル', 'some-track-td','100', 'Artist - Name: YOASOBI, ID: some-random-id')]"
    assert str(test_playlist) == expected


def test_playlist_repr():
    test_playlist = playlist.Playlist(test_playlist_name, test_playlist_id, test_playlist_description)
    expected = "Playlist(Anime Now, some-playlist-id, An anime playlist, [])"
    assert repr(test_playlist) == expected


def test_playlist_add_repr():
    test_playlist = playlist.Playlist(test_playlist_name, test_playlist_id, test_playlist_description)
    test_playlist.add(test_track)
    expected = "Playlist(Anime Now, some-playlist-id, An anime playlist, [Track('アイドル', 'some-track-td','100', 'Artist - Name: YOASOBI, ID: some-random-id')])"
    assert repr(test_playlist) == expected
