class Artist(object):
    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id

    def __str__(self) -> str:
        return "Artist - Name: {}, ID: {}".format(self.name, self.id)

    def __repr__(self) -> str:
        return f"Artist('{self.name}', '{self.id}')"

    def __eq__(self, other) -> bool:
        """Overrides the default implementation"""
        if isinstance(other, Artist):
            return self.name == other.name and self.id == other.id
        return False
