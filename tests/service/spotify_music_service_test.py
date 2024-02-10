import random
from unittest.mock import Mock, patch
from model.spotify import spotify_playlist

from service.spotify_music_service import SpotifyMusicService


@patch("dao.spotify.spotify_playlist_dao.SpotifyPlaylistDAO")
def test_ctor(mock_spotify):
    music_service = SpotifyMusicService(mock_spotify)
    assert music_service.dao == mock_spotify


@patch("spotipy.Spotify")
def test_get_current_user_playlists_no_playlists(mock_spotify):
    mock_ids = []
    mock_spotify.get_all_playlists = Mock(return_value=mock_ids)
    music_service = SpotifyMusicService(mock_spotify)
    current_user_playlists = music_service.get_current_user_playlists()
    assert current_user_playlists.playlists == []


@patch("spotipy.Spotify")
def test_get_current_user_playlists_single_playlist(mock_spotify):
    mock_ids = [spotify_playlist.SpotifyPlaylistId("some-spotify-id")]
    mock_spotify.get_all_playlists = Mock(return_value=mock_ids)
    expected_playlist = spotify_playlist.SpotifyPlaylist("some-playlist", mock_ids[0], "some description", [])
    mock_playlist = Mock(return_value=expected_playlist)
    mock_spotify.get_playlist = mock_playlist
    music_service = SpotifyMusicService(mock_spotify)
    current_user_playlists = music_service.get_current_user_playlists()
    assert current_user_playlists.playlists == [expected_playlist]


@patch("spotipy.Spotify")
def test_get_current_user_playlists_multiple_playlists(mock_spotify):
    expected_playlists = [generate_playlist(num=1), generate_playlist(num=2)]
    mock_playlist_ids = [expected_playlists[0].id, expected_playlists[1].id]
    mock_spotify.get_all_playlists = Mock(return_value=mock_playlist_ids)
    mock_spotify.get_playlist = get_playlist_side_effect
    music_service = SpotifyMusicService(mock_spotify)
    current_user_playlists = music_service.get_current_user_playlists()
    assert len(current_user_playlists.playlists) == 2


def get_playlist_side_effect(value: spotify_playlist.SpotifyPlaylistId):
    if value == spotify_playlist.SpotifyPlaylistId("1"):
        return generate_playlist(num=1)
    elif value == spotify_playlist.SpotifyPlaylistId("2"):
        return generate_playlist(num=2)


def generate_playlist(num: int = random.randint(0, 1000)) -> spotify_playlist.SpotifyPlaylist:
    playlist_id = spotify_playlist.SpotifyPlaylistId(f"{num}")
    return spotify_playlist.SpotifyPlaylist(f"Playlist #{num}", playlist_id, "another playlist for the books", [])
