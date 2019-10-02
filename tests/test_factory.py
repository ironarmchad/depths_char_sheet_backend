from app import create_app


def test_config():
    assert not create_app('dev').testing
    assert create_app('testing').testing
