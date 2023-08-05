import pytest
import requests

from pybiomart import base

# pylint: disable=redefined-outer-name, no-self-use


@pytest.fixture
def default_url():
    """Default URL fixture."""
    return '{}:{}{}'.format(base.DEFAULT_HOST, base.DEFAULT_PORT,
                            base.DEFAULT_PATH)


# pylint: disable=no-self-use
class TestBase(object):
    """Tests for ServerBase class."""

    def test_basic(self, default_url):
        """Tests default instantation."""

        base_obj = base.ServerBase()

        assert base_obj.host == base.DEFAULT_HOST
        assert base_obj.path == base.DEFAULT_PATH
        assert base_obj.port == base.DEFAULT_PORT
        assert base_obj.use_cache
        assert base_obj.url == default_url

    def test_params(self):
        """Tests instantation with custom args."""

        base_obj = base.ServerBase(
            host='http://www.ensembl.org',
            path='/other/path',
            port=8080,
            use_cache=False)

        assert base_obj.host == 'http://www.ensembl.org'
        assert base_obj.path == '/other/path'
        assert base_obj.port == 8080
        assert not base_obj.use_cache
        assert base_obj.url == 'http://www.ensembl.org:8080/other/path'

    def test_missing_http(self):
        """Tests url with missing http."""

        base_obj = base.ServerBase(host='www.ensembl.org')
        assert base_obj.host == 'http://www.ensembl.org'

    def test_trailing_slash(self):
        """Tests url with trailing slash."""

        base_obj = base.ServerBase(host='http://www.ensembl.org/')
        assert base_obj.host == 'http://www.ensembl.org'

    def test_get(self, mocker, default_url):
        """Tests get invocation."""

        req = pytest.helpers.mock_response()

        mock_get = mocker.patch.object(requests, 'get', return_value=req)

        base_obj = base.ServerBase()
        base_obj.get()

        mock_get.assert_called_once_with(default_url, params={})

    def test_get_with_params(self, mocker, default_url):
        """Tests get invocation with custom parameters."""

        req = pytest.helpers.mock_response()

        mock_get = mocker.patch.object(requests, 'get', return_value=req)

        base_obj = base.ServerBase()
        base_obj.get(test=True)

        mock_get.assert_called_once_with(default_url, params={'test': True})
