from adaptor import local_storage
from model import playlist


class MigratorData(local_storage.LocalSerializable):
    def __init__(self, local_file_name: str):
        super().__init__(local_file_name)
        if self.data is None:
            self.data = {}

    def add_playlist(self, playlist: playlist.Playlist) -> None:
        if self.contains_playlist(playlist):
            raise AlreadyProcessedException(playlist)
        self.data[playlist.id] = playlist

    def remove_playlist(self, playlist: playlist.Playlist) -> None:
        if not self.contains_playlist(playlist):
            raise NoSuchPlaylistException(playlist)

    def contains_playlist(self, playlist: playlist.Playlist) -> bool:
        return playlist.id in self.data

    def __eq__(self, other) -> bool:
        if isinstance(other, MigratorData):
            if len(self.data) == len(other.data):
                for id, playlist in self.data.items():
                    if not other.data[id] == playlist:
                        return False
                return True
        return False


class AlreadyProcessedException(Exception):
    def __init__(self, playlist: playlist.Playlist):
        super().__init__(f"already processed: {playlist}")


class NoSuchPlaylistException(Exception):
    def __init__(self, playlist: playlist.Playlist):
        super().__init__(f"no such playlist: {playlist}")
