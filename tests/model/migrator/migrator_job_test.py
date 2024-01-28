from model import artist, track
from model.migrator import migrator_job
from model.spotify import spotify_playlist
from model.youtube import youtube_playlist

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
