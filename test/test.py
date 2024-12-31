# test/test.py

import os
import pytest
import entrypoint
from entrypoint import create_linode
from linode_api4 import ApiError
from unittest.mock import patch
from .helpers import (
    assert_request,
    assert_instance
)


def test_linode_instance(mock_LinodeClient, mock_post):
    with patch('entrypoint.LinodeClient', side_effect=mock_LinodeClient) as f:

        # test the create_linode method
        linode = create_linode()

        assert str(linode) == 'Instance: 12345'
        assert_instance(f, '12345')

        # verify the post request
        assert_request(mock_post)


def test_linode_instance_err(mock_LinodeClient, mock_post_err):
    with patch('entrypoint.LinodeClient', side_effect=mock_LinodeClient) as f:
        with pytest.raises(ApiError, match="401: Invalid Token;") as e:
            # validate api token error
            linode = create_linode()  # noqa: F841

        assert_instance(f, '12345')
        assert e.value.status == 401
        assert e.value.errors == ["Invalid Token"]
        assert_request(mock_post_err)


def test_integration(mock_LinodeClient, mock_post, mock_output_file, capsys):
    with patch('entrypoint.LinodeClient', side_effect=mock_LinodeClient):
        try:
            open(os.environ['GITHUB_OUTPUT'], 'a').close()
        except KeyError:
            os.environ['GITHUB_OUTPUT'] = str(mock_output_file)

        entrypoint.main()

    captured = capsys.readouterr()
    assert captured.out == 'linode-id=12345\n\n'
