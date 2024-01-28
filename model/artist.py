class Artist(object):
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def __str__(self) -> str:
        return "Artist - Name: {}, ID: {}".format(self.name, self.id)

    def __repr__(self) -> str:
        return f"Artist('{self.name}', '{self.id}')"
