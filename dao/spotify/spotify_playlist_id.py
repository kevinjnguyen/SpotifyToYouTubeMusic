class SpotifyPlaylistId:
    def __init__(self, id: str):
        self.id = id

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SpotifyPlaylistId):
            return self.id == __value.id
        return True
