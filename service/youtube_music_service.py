import time
from typing import Dict, List
import ytmusicapi
from model import track
from model.youtube import youtube_playlist


class YoutubeMusicService(object):
    oauth_file_name = "oauth.json"
    default_retry_attempts = 3

    def __init__(self, auth_param: str = oauth_file_name, retry_attempts: int = default_retry_attempts):
        self.ytmusic = ytmusicapi.YTMusic(auth_param)
        self.retry_attempts = retry_attempts

    def create_playlist(self, name: str, description: str) -> youtube_playlist.YoutubePlaylist:
        attempt = 1
        while True:
            try:
                playlist_id = self.ytmusic.create_playlist(name, description)
                return youtube_playlist.YoutubePlaylist(name, playlist_id, description)
            except Exception as e:
                if attempt == self.retry_attempts:
                    raise e
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1

    def search_track(self, query: track.Track) -> str:
        attempt = 1
        while True:
            try:
                query = "{} by {}".format(query.name, query.artist.name)
                api_search_results = self.ytmusic.search(query=query, filter="songs")
                return YoutubeMusicService.select_track_id_from_query_results(api_search_results)
            except NoSongFoundException as e:
                raise e
            except Exception as e:
                if attempt == self.retry_attempts:
                    raise e
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1

    def delete_playlist(self, playlist_id: str) -> None:
        self.ytmusic.delete_playlist(playlist_id)

    def select_track_id_from_query_results(api_search_results: List[Dict]) -> str:
        if len(api_search_results) == 0:
            raise NoSongFoundException(track)
        return api_search_results[0]["videoId"]

    def add_song_to_playlist(self, query: track.Track, playlist: youtube_playlist.YoutubePlaylist) -> None:
        return self.add_songs_to_playlist([query], playlist)

    def add_songs_to_playlist(self, query: List[track.Track], playlist: youtube_playlist.YoutubePlaylist) -> None:
        attempt = 1
        while True:
            try:
                video_ids = []
                for qt in query:
                    video_id = self.search_track(qt)
                    video_ids.append(video_id)

                self.ytmusic.add_playlist_items(playlistId=playlist.id, videoIds=video_ids)
                return
            except NoSongFoundException as e:
                raise e
            except Exception as e:
                if attempt == self.retry_attempts:
                    raise e
                amount_to_sleep = 1 * (attempt)
                time.sleep(amount_to_sleep)
                attempt += 1


class NoSongFoundException(Exception):
    def __init__(self, track):
        self.add_note("unable to find results for: {}".format(track))
