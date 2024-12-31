# test/helpers.py

from .constants import (
    MockHTTP,
    Path
)


def assert_instance(mocked_instance: any, token: str):
    mocked_instance.assert_called_once()
    mocked_instance.assert_called_with(token)


def assert_request(mocked_method: any):
    args, kwargs = mocked_method.call_args
    assert Path.ENDPOINT in args
    assert MockHTTP.HEADERS == kwargs['headers']
    assert Path.CA_PATH == kwargs['verify']
