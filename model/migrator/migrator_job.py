from typing import Dict, List, Self
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

    def __init__(self, from_playlist: spotify_playlist.SpotifyPlaylist, to_playlist: youtube_playlist.YouTubePlaylist):
        self.from_playlist = from_playlist
        self.to_playlist = to_playlist
        self.current_track_index = 0

    def successful(self) -> None:
        self.current_track_index += 1

    def is_complete(self) -> bool:
        return len(self.from_playlist.tracks) == self.current_track_index


class JobsData(object):
    jobs: Dict[str, Job]

    def __init__(self, jobs: List[Job]):
        self.jobs = {}
        for job in jobs:
            if job.from_playlist.id in jobs:
                raise DuplicateFromPlaylistException(job.from_playlist.id)
            else:
                self.jobs[job.from_playlist.id] = job

    def get_job(self, from_playlist: spotify_playlist.SpotifyPlaylist) -> Job:
        if from_playlist.id in self.jobs:
            return self.jobs[from_playlist.id]
        raise NoSuchJobException(from_playlist.id)


class JobsBuilder(object):
    jobs: List[Job]

    def __init__(self, jobs: List[Job] = []):
        self.jobs = jobs

    def add_job(self, job: Job) -> Self:
        self.jobs.append(job)
        return self

    def build(self) -> JobsData:
        return JobsData(self.jobs)
