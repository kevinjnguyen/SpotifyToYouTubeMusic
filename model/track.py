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
