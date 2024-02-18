import time
from typing import Any, Dict, List
import ytmusicapi
from dao.youtube import youtube_track_id
from model import track

from model.youtube import youtube_playlist


class YoutubeDAOException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidDAOConfiguration(YoutubeDAOException):
    def __init__(self, msg: str):
        super().__init__(msg)


class NoSongFoundException(Exception):
    def __init__(self, track):
        self.track = track


class YoutubeMusicDAO:

    default_retry_attempts = 3

    def __init__(self, api: ytmusicapi.YTMusic, retry_attempts: int = default_retry_attempts):
        self.api = api
        self.retry_attempts = retry_attempts
        self.__verify_args()

    def __verify_args(self):
        if self.retry_attempts <= 0:
            raise InvalidDAOConfiguration("number of retries must be gte to 0")

    def create_playlist(self, name: str, description: str) -> youtube_playlist.YoutubePlaylist:
        attempt = 0
        while True:
            try:
                playlist_id = self.api.create_playlist(name, description)
                return youtube_playlist.YoutubePlaylist(name, playlist_id, description)
            except Exception as e:
                if attempt >= self.retry_attempts:
                    raise YoutubeDAOException(e)
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1

    def search_track(self, search_track: track.Track) -> youtube_track_id.YoutubeTrackID:
        attempt = 0
        while True:
            try:
                query = "{} by {}".format(search_track.name, search_track.artist.name)
                api_search_results = self.api.search(query=query, filter="songs")
                return self.__select_track_id_from_query_results(api_search_results)
            except NoSongFoundException as e:
                raise e
            except Exception as e:
                if attempt >= self.retry_attempts:
                    raise YoutubeDAOException(e)
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1

    def delete_playlist(self, playlist: youtube_playlist.YoutubePlaylist) -> None:
        self.api.delete_playlist(playlist.id)

    def add_song_to_playlist(self, query: track.Track, playlist: youtube_playlist.YoutubePlaylist) -> None:
        attempt = 0
        while True:
            try:
                # TODO: Future optimization: Batch add to playlists.
                video_ids = [self.search_track(query)]
                self.api.add_playlist_items(playlistId=playlist.id, videoIds=video_ids)
                return
            except NoSongFoundException as e:
                raise e
            except Exception as e:
                if attempt >= self.retry_attempts:
                    raise e
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1

    def __select_track_id_from_query_results(
        self, api_search_results: List[Dict[str, Any]]
    ) -> youtube_track_id.YoutubeTrackID:
        if len(api_search_results) == 0:
            raise NoSongFoundException(track)
        return youtube_track_id.YoutubeTrackID(api_search_results[0]["videoId"])
