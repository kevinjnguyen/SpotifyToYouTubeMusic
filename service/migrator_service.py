import logging
from model.migrator.migrator_data import MigratorData, MigratorState
from model.playlist import Playlist

from service.spotify_music_service import SpotifyMusicService
from service.youtube_music_service import NoSongFoundException, YoutubeMusicService


logger = logging.getLogger(__name__)


class MigratorServiceException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class MigratorService:

    def __init__(self, spotify: SpotifyMusicService, youtube: YoutubeMusicService, migrator_state_file: str):
        self.spotify = spotify
        self.youtube = youtube
        self.migrator_data = MigratorData(migrator_state_file)
        if self.__should_populate():
            self.__populate_migrator()
            self.migrator_data.save()

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

    def migrate_playlist(self, spotify_playlist: Playlist):
        plog = logger.getChild(spotify_playlist.id)
        plog.info(f"Migrating playlist: {spotify_playlist.name}")
        youtube_playlist = self.youtube.create_playlist(spotify_playlist.name, spotify_playlist.description)
        successful = True
        for track in spotify_playlist.tracks:
            try:
                self.youtube.add_song_to_playlist(track, youtube_playlist)
            except NoSongFoundException:
                plog.warning(f"Unable to find track: {track}")
            except Exception as e:
                plog.error(f"Failed to process playlist due to: {e}")
                successful = False

        if successful:
            self.migrator_data.success(spotify_playlist.id)
        else:
            self.migrator_data.failure(spotify_playlist.id)

        self.migrator_data.save()

    def migrate_all_playlists(self):
        if self.migrator_data.get_state() != MigratorState.POPULATED:
            raise MigratorServiceException("migrator must be in populated state to migrate")

        for _, playlist in self.migrator_data.data.playlists.items():
            if playlist.id in self.migrator_data.data.already_processed:
                logger.info(f"Already processed playlist: {playlist.name}")
            elif playlist.id in self.migrator_data.data.failed:
                logger.info(f"Playlist previously failed: {playlist.name}")
            else:
                self.migrate_playlist(playlist)
