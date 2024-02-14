import random
import tempfile
from unittest.mock import Mock, patch
from model.migrator.migrator_data import MigratorState
from model.spotify import spotify_playlist
from service.migrator_service import MigratorService
from service.spotify_music_service import CurrentUserPlaylists


def generate_playlist(num: int = random.randint(0, 1000)) -> spotify_playlist.SpotifyPlaylist:
    playlist_id = spotify_playlist.SpotifyPlaylistId(f"{num}")
    return spotify_playlist.SpotifyPlaylist(f"Playlist #{num}", playlist_id, "another playlist for the books", [])


empty_user_playlists = CurrentUserPlaylists([])
single_user_playlists = CurrentUserPlaylists([generate_playlist(1)])


@patch("service.spotify_music_service.SpotifyMusicService")
def test_migrator_service(spotify):
    migrator_file = tempfile.NamedTemporaryFile()
    migrator_file.close()

    spotify.get_current_user_playlists = Mock(return_value=empty_user_playlists)
    migrator_service = MigratorService(spotify, migrator_file.name)
    assert migrator_service.spotify == spotify
    assert len(migrator_service.migrator_data.data.playlists) == 0
    assert migrator_service.migrator_data.data.state == MigratorState.POPULATED


@patch("service.spotify_music_service.SpotifyMusicService")
def test_migrator_service_populates_migrator(spotify):
    migrator_file = tempfile.NamedTemporaryFile()
    migrator_file.close()

    spotify.get_current_user_playlists = Mock(return_value=single_user_playlists)
    migrator_service = MigratorService(spotify, migrator_file.name)
    assert migrator_service.migrator_data.contains_playlist(single_user_playlists.playlists[0]) == True
    assert migrator_service.migrator_data.get_state() == MigratorState.POPULATED


@patch("service.spotify_music_service.SpotifyMusicService")
def test_migrator_service_migrate_all_playlists_checks_state(spotify):
    migrator_file = tempfile.NamedTemporaryFile()
    migrator_file.close()
    spotify.get_current_user_playlists = Mock(return_value=single_user_playlists)
    migrator_service = MigratorService(spotify, migrator_file.name)
    migrator_service.migrate_all_playlists()


def get_current_user_playlists_empty_side_effect():
    return empty_user_playlists


def get_current_user_playlists_single_side_effect():
    return CurrentUserPlaylists([generate_playlist(1)])
