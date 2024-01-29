from typing import Any
from adaptor.local_storage import LocalSerializable
import tempfile


class TestLocalModel(LocalSerializable):
    def __init__(self, path: str, data: Any):
        super().__init__(path, data=data)


def test_local_serializable_reads():
    tf = tempfile.NamedTemporaryFile()
    tf.close()

    local_model = TestLocalModel(tf.name, data={})
    local_model.data["test_key"] = "test_value"
    local_model.save()

    loaded_local_model = TestLocalModel(tf.name, data={})
    assert loaded_local_model.data["test_key"] == "test_value"


class TestNestedModel(object):
    def __init__(self):
        self.random_internal_data = "some-internal-value"
        self.mapping = {"test": "value"}
        self.data = 0


def test_local_serializable_custom_types():
    tf = tempfile.NamedTemporaryFile()
    tf.close()

    local_model = TestLocalModel(tf.name, data=TestNestedModel())
    local_model.save()

    loaded_local_model = TestLocalModel(tf.name, data=TestNestedModel())
    assert loaded_local_model.data.random_internal_data == "some-internal-value"
    assert loaded_local_model.data.mapping == {"test": "value"}
    assert loaded_local_model.data.data == 0
