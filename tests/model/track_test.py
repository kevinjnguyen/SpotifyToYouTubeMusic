from model import artist, track


test_artist_name = "YOASOBI"
test_artist_id = "some-random-id"
test_artist = artist.Artist(test_artist_name, test_artist_id)
test_track_name = "アイドル"
test_track_id = "some-track-td"
test_duration = 100


def test_track_str():
    test_track = track.Track(test_track_name, test_track_id, test_duration, test_artist)
    expected = "Track - Name: アイドル, ID: some-track-td, Duration (MS): 100, Artist: Artist - Name: YOASOBI, ID: some-random-id"
    assert str(test_track) == expected


def test_track_repr():
    test_track = track.Track(test_track_name, test_track_id, test_duration, test_artist)
    expected = "Track('アイドル', 'some-track-td','100', 'Artist - Name: YOASOBI, ID: some-random-id')"
    assert repr(test_track) == expected
