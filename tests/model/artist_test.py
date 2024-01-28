from model.artist import Artist


test_artist = "YOASOBI"
test_id = "some-random-id"


def test_artist_str():

    artist = Artist(test_artist, test_id)
    expected = "Artist - Name: YOASOBI, ID: some-random-id"
    assert str(artist) == expected


def test_artist_repr():
    artist = Artist(test_artist, test_id)
    expected = "Artist('YOASOBI', 'some-random-id')"
    assert repr(artist) == expected
