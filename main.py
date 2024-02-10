import logging
import sys

from model.migrator import migrator_data
from service import spotify_music_service, youtube_music_service, migrator_service


def main():
    spotify = spotify_music_service.SpotifyMusicService()
    # youtube = youtube_music_service.YoutubeMusicService()
    # migrator = migrator_service.MigratorService(spotify, youtube)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())  # next section explains the use of sys.exit
