from model import artist


class Track(object):
    def __init__(self, name: str, id: str, duration: int, artist: artist.Artist):
        self.name = name
        self.id = id
        self.artist = artist
        self.duration = duration

    def __str__(self) -> str:
        return f"Track - Name: {self.name}, ID: {self.id}, Duration (MS): {self.duration}, Artist: {self.artist}"

    def __repr__(self) -> str:
        return f"Track('{self.name}', '{self.id}','{self.duration}', '{self.artist}')"

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, Track):
            return (
                self.name == other.name
                and self.id == other.id
                and self.artist == other.artist
                and self.duration == other.duration
            )
        return False


class NoArtistException(Exception):
    def __init__(self):
        super().__init__()


class InvalidTrackException(Exception):
    def __init__(self, field_name: str):
        super().__init__(f"missing field: {field_name}")
