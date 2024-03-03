import logging
import sys

from service import spotify_music_service, youtube_music_service, migrator_service


def main():
    spotify = spotify_music_service.SpotifyMusicService()
    youtube = youtube_music_service.YoutubeMusicService()
    migrator = migrator_service.MigratorService(spotify, youtube, "migrator_data.db")
    migrator.migrate_all_playlists()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())  # next section explains the use of sys.exit
