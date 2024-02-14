import logging
from model.migrator.migrator_data import MigratorData, MigratorState

from service.spotify_music_service import SpotifyMusicService


logger = logging.getLogger(__name__)


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
        self.migrator_data.set_populated()
