import logging
from model.migrator.migrator_data import MigratorData, MigratorState
from model.spotify.spotify_playlist import SpotifyPlaylist

from service.spotify_music_service import SpotifyMusicService


logger = logging.getLogger(__name__)


class MigratorServiceException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MigratorService:

    def __init__(self, spotify: SpotifyMusicService, migrator_state_file: str):
        self.spotify = spotify
        self.migrator_data = MigratorData(migrator_state_file)
        if self.__should_populate():
            self.__populate_migrator()

    def __should_populate(self):
        state = self.migrator_data.get_state()
        if state == MigratorState.NONE:
            return True
        return False

    def __populate_migrator(self):
        current_user_playlists = self.spotify.get_current_user_playlists()
        for playlist in current_user_playlists.playlists:
            if not self.migrator_data.contains_playlist(playlist):
                self.migrator_data.add_playlist(playlist)
        logger.info(f"Successfully populated: {len(self.migrator_data.data.playlists)} playlists.")
        self.migrator_data.set_populated()

    def migrate_playlist(self, spotify_playlist: SpotifyPlaylist):
        pass

    def migrate_all_playlists(self):
        if self.migrator_data.get_state() != MigratorState.POPULATED:
            raise MigratorServiceException("migrator must be in populated state to migrate")

        for _, playlist in self.migrator_data.data.playlists.items():
            self.migrate_playlist(playlist)
        