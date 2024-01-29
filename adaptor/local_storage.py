import os
import pickle
from typing import Any


class LocalSerializable(object):
    data: Any

    def __init__(self, local_file_name: str, data: Any = None):
        self.local_file_name = local_file_name
        self.load(data)

    def save(self) -> None:
        local_file = open(self.local_file_name, "wb")
        pickle.dump(self.data, local_file)
        local_file.close()

    def load(self, data: Any) -> None:
        if os.path.exists(self.local_file_name):
            local_file = open(self.local_file_name, "rb")
            self.data = pickle.load(local_file)
            local_file.close()
        else:
            self.data = data
