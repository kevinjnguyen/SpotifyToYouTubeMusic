from model import artist, track
from model.migrator import migrator_job
from model.spotify import spotify_playlist
from model.youtube import youtube_playlist

import pytest

test_spotify_playlist = spotify_playlist.SpotifyPlaylist("from-spotify", "some-spotify-id", "some-spotify-description")
test_youtube_playlist = youtube_playlist.YouTubePlaylist("to-youtube", "some-youtube-id", "some-youtube-description")


def test_job():
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    assert new_job.current_track_index == 0
    assert new_job.from_playlist == test_spotify_playlist
    assert new_job.to_playlist == test_youtube_playlist


def test_job_successful():
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    new_job.successful()
    assert new_job.current_track_index == 1


def test_job_is_complete():
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    assert new_job.is_complete() == True


def test_job_is_complete_with_tracks():
    test_spotify_playlist = spotify_playlist.SpotifyPlaylist(
        "from-spotify", "some-spotify-id", "some-spotify-description"
    )
    test_artist_name = "YOASOBI"
    test_artist_id = "some-random-id"
    test_artist = artist.Artist(test_artist_name, test_artist_id)
    test_track_name = "アイドル"
    test_track_id = "some-track-td"
    test_duration = 100
    test_track = track.Track(test_track_name, test_track_id, test_duration, test_artist)

    test_spotify_playlist.add(test_track)
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    assert new_job.is_complete() == False
    new_job.successful()
    assert new_job.is_complete() == True


def test_jobs_data():
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    jobs_data = migrator_job.JobsData([new_job])
    assert len(jobs_data.jobs) == 1
    assert jobs_data.jobs[test_spotify_playlist.id] == new_job

    fetched_job = jobs_data.get_job(test_spotify_playlist)
    assert fetched_job == new_job

    with pytest.raises(Exception) as e_info:
        new_playlist = spotify_playlist.SpotifyPlaylist("from-spotify", "some-other-id", "some-spotify-description")
        jobs_data.get_job(new_playlist)


def test_jobs_data_builder():
    jobs_data_builder = migrator_job.JobsBuilder()
    new_job = migrator_job.Job(test_spotify_playlist, test_youtube_playlist)
    jobs_data_builder.add_job(new_job)
    jobs_data = jobs_data_builder.build()
    assert len(jobs_data.jobs) == 1
    assert jobs_data.jobs[test_spotify_playlist.id] == new_job
