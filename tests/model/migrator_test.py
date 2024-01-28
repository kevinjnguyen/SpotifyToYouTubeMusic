from model.Migrator import Migrator


def test_migrator_ctor_sets_test_value():
    migrator = Migrator()
    assert migrator.test_value == 'my_value'
