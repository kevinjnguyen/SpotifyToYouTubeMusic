import logging
import traceback
from typing import List, Optional
from model.migrator import migrator_data
from model.spotify import spotify_playlist
from service import spotify_music_service, youtube_music_service

default_migrator_file = "migrator.data"

logger = logging.getLogger(__name__)


class MigratorService(object):
    def __init__(
        self,
        spotify: spotify_music_service.SpotifyMusicService,
        youtube: youtube_music_service.YoutubeMusicService,
        local_migrator_file=default_migrator_file,
    ):
        self.spotify = spotify
        self.youtube = youtube
        self.migrator = migrator_data.MigratorData(local_file_name=local_migrator_file)
        self.failures = {}
        self.num_playlists = self.spotify.get_playlists_count()
        self.populate()

    def should_fetch_playlists(self) -> bool:
        return len(self.migrator.data) + len(self.failures) < self.num_playlists

    def populate(self) -> None:
        logger.info("Fetching playlists from Spotify")
        self.num_playlists = self.spotify.get_playlists_count()
        logger.info(f"Total number of requested playlists: {self.num_playlists}")
        if len(self.migrator.data) > 0:
            logger.info(f"Resuming from: {len(self.migrator.data)} / {self.num_playlists}")

        while self.should_fetch_playlists():
            logger.info("Starting next batch: ")
            try:
                initial_offset = len(self.migrator.data)
                user_playlists = self.spotify.get_playlists(
                    initial_offset=initial_offset, ignore_list=set(self.failures.keys())
                )
                for playlist in user_playlists:
                    if not self.migrator.contains_playlist(playlist):
                        self.migrator.add_playlist(playlist)
            except spotify_music_service.PlaylistProcessingException as e:
                logger.error(f"Exception while processing: {e.playlist_name}. Adding to ignore list and continuing")
                self.failures[e.playlist_id] = e
            finally:
                logger.info(f"-- Number of playlists for migration: {len(self.migrator.data) - len(self.failures)}")
                logger.info(f"-- Number of ignored playlists: {len(self.failures)}")
                self.migrator.save()

