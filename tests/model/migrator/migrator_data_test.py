import tempfile
from model import playlist

from model.migrator import migrator_data


def test_migrator_data():
    tf = tempfile.NamedTemporaryFile()
    tf.close()
    md = migrator_data.MigratorData(tf.name)
    assert md.data == {}
    tp = playlist.Playlist("test-playlist", "some-id", "description")
    md.add_playlist(tp)
    md.save()

    local_md = migrator_data.MigratorData(tf.name)
    assert local_md == md