from unittest.mock import patch
from dao.youtube.youtube_playlist_dao import (
    InvalidDAOConfiguration,
    NoSongFoundException,
    YoutubeDAOException,
    YoutubeMusicDAO,
)
from dao.youtube.youtube_track_id import YoutubeTrackID
from model import artist, track
from model.youtube import youtube_playlist
from model.youtube.youtube_playlist import YoutubePlaylist

import pytest


@patch("ytmusicapi.YTMusic")
def test_ctor(yt):
    dao = YoutubeMusicDAO(yt)
    assert dao.api == yt
    assert dao.retry_attempts == YoutubeMusicDAO.default_retry_attempts

    num_attempts = 10
    dao = YoutubeMusicDAO(yt, retry_attempts=num_attempts)
    assert dao.api == yt
    assert dao.retry_attempts == num_attempts

    with pytest.raises(InvalidDAOConfiguration):
        dao = YoutubeMusicDAO(yt, retry_attempts=-1)


@patch("ytmusicapi.YTMusic")
def test_create_playlist(yt):
    playlist_name = "some-playlist"
    playlist_description = "some-description"
    yt.create_playlist = create_playlist_side_effect
    dao = YoutubeMusicDAO(yt)
    yt_playlist = dao.create_playlist(playlist_name, playlist_description)
    assert yt_playlist == YoutubePlaylist(playlist_name, "playlist-id", playlist_description)


@patch("ytmusicapi.YTMusic")
def test_create_playlist_throws_exception_exceeding_attempts(yt):
    yt.create_playlist = create_playlist_failed_side_effect
    dao = YoutubeMusicDAO(yt, retry_attempts=1)
    with pytest.raises(YoutubeDAOException):
        dao.create_playlist("some-deplaylist", "some-description")


@patch("ytmusicapi.YTMusic")
def test_search_track(yt):
    test_track = track.Track("some-track", "some-id", 123, artist.Artist("some-artist", "some-id-art"))
    yt.search = search_track_side_effect
    dao = YoutubeMusicDAO(yt)
    search_track_id = dao.search_track(test_track)
    assert search_track_id == YoutubeTrackID("abcdef")


@patch("ytmusicapi.YTMusic")
def test_search_track_no_song_found(yt):
    test_track = track.Track("some-track", "some-id", 123, artist.Artist("some-artist", "some-id-art"))
    yt.search = search_tracks_no_songs_side_effect
    dao = YoutubeMusicDAO(yt)
    with pytest.raises(NoSongFoundException):
        dao.search_track(test_track)


@patch("ytmusicapi.YTMusic")
def test_add_song_to_playlist(yt):
    test_track = track.Track("some-track", "some-id", 123, artist.Artist("some-artist", "some-id-art"))
    test_playlist = youtube_playlist.YoutubePlaylist("some-playlist", "some-id", "some-description")
    yt.search = search_track_side_effect
    dao = YoutubeMusicDAO(yt)
    dao.add_song_to_playlist(test_track, test_playlist)
    assert yt.add_playlist_items.called


@patch("ytmusicapi.YTMusic")
def test_add_song_to_playlist_no_songs_found(yt):
    test_track = track.Track("some-track", "some-id", 123, artist.Artist("some-artist", "some-id-art"))
    test_playlist = youtube_playlist.YoutubePlaylist("some-playlist", "some-id", "some-description")
    yt.search = search_tracks_no_songs_side_effect
    dao = YoutubeMusicDAO(yt)
    with pytest.raises(NoSongFoundException):
        dao.add_song_to_playlist(test_track, test_playlist)


def create_playlist_side_effect(name, description):
    return "playlist-id"


def create_playlist_failed_side_effect(name, description):
    raise Exception("a youtube music exception")


def search_track_side_effect(query, filter):
    return [{"videoId": "abcdef"}]


def search_tracks_no_songs_side_effect(query, filter):
    return []
