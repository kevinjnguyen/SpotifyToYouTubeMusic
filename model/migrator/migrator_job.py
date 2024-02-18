from typing import List, Optional, Self
from adaptor import local_storage
from model.spotify import spotify_playlist
from model.youtube import youtube_playlist


class DuplicateFromPlaylistException(Exception):
    def __init__(self, playlist_id: str):
        super().__init__(f"an existing job already exists with playlist id: {playlist_id}")


class NoSuchJobException(Exception):
    def __init__(self, playlist_id: str):
        super().__init__(f"no migration job with id: {playlist_id}")


class Job(object):
    from_playlist: spotify_playlist.SpotifyPlaylist

    def __init__(self, from_playlist: spotify_playlist.SpotifyPlaylist, to_playlist: youtube_playlist.YoutubePlaylist):
        self.from_playlist = from_playlist
        self.to_playlist = to_playlist
        self.current_track_index = 0

    def successful(self) -> None:
        self.current_track_index += 1

    def is_complete(self) -> bool:
        return len(self.from_playlist.tracks) == self.current_track_index

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, Job):
            return (
                self.from_playlist == other.from_playlist
                and self.to_playlist == other.to_playlist
                and self.current_track_index == other.current_track_index
            )

        return False


class JobsData(local_storage.LocalSerializable):
    def __init__(self, local_file_name: str, jobs: Optional[List[Job]] = None):
        super().__init__(local_file_name)
        if self.data is None and jobs is not None:
            self.data = {}
            for job in jobs:
                if job.from_playlist.id in self.data:
                    raise DuplicateFromPlaylistException(job.from_playlist.id.id)
                else:
                    self.data[job.from_playlist.id] = job

    def get_job(self, from_playlist: spotify_playlist.SpotifyPlaylist) -> Job:
        if self.data is not None and from_playlist.id in self.data:
            return self.data[from_playlist.id]
        raise NoSuchJobException(from_playlist.id.id)


class JobsBuilder(object):
    jobs: List[Job]

    def __init__(self, jobs: List[Job] = [], local_file_name: str = "jobs.data"):
        self.jobs = jobs
        self.local_file_name = local_file_name

    def add_job(self, job: Job) -> Self:
        self.jobs.append(job)
        return self

    def build(self) -> JobsData:
        return JobsData(self.local_file_name, self.jobs)
