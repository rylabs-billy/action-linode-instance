# test/conftest.py

import os
import pytest
import json
from linode_api4 import LinodeClient
from unittest.mock import (
    Mock,
    patch
)
from .constants import (
    MockHTTP,
    Path
)


@pytest.fixture
def mock_output_file(tmp_path):
    file_path = tmp_path / 'tmpfile'
    open('tmpfile', 'a').close()
    yield file_path

    if os.path.exists('tmpfile'):
        os.remove('tmpfile')


@pytest.fixture(scope='session')
def mock_response():
    def _build(
            status_code: int = 201,
            data: dict = {},
            headers: dict = {}
    ) -> any:
        _data = json.dumps(data)
        # setup mocks
        resp = Mock()
        resp.status_code = status_code
        resp.content = bytes(_data, 'utf-8')
        resp.text = _data
        resp.json = lambda: json.loads(_data)
        resp.headers = headers

        return resp

    yield _build


@pytest.fixture(scope="function")
def mock_client():
    with patch.object(LinodeClient, "_user_agent", "test-client"):
        client = LinodeClient('12345')
        client.session = Mock()
        client.session.post.return_value = None
        client.ca_path = Path.CA_PATH

        yield client


@pytest.fixture(scope="function")
def mock_post(mock_client, mock_response):
    mock_client.session.post.return_value = mock_response(
        status_code=201,
        headers=MockHTTP.HEADERS,
        data=MockHTTP.RESP
    )

    yield mock_client.session.post


@pytest.fixture(scope="function")
def mock_post_err(mock_client, mock_response):
    mock_client.session.post.return_value = mock_response(
        status_code=401,
        headers=MockHTTP.HEADERS,
        data=MockHTTP.ERR_RESP
    )

    yield mock_client.session.post


@pytest.fixture(scope='function')
def mock_LinodeClient(mock_client):
    def _build(token) -> any:
        if token:
            return mock_client

    yield _build
