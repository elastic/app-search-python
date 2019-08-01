from unittest import TestCase, skipIf
from requests.status_codes import codes
from future.utils import iteritems
import requests_mock

import elastic_app_search
from elastic_app_search.request_session import RequestSession
from elastic_app_search.exceptions import InvalidCredentials


class TestRequestSession(TestCase):

    api_host_key = 'api_host_key'

    def setUp(self):
        self.session = RequestSession(self.api_host_key, 'http://www.base_url.com')

    def test_request_success(self):
        expected_return = {'foo': 'bar'}
        endpoint = 'some_endpoint'

        with requests_mock.Mocker() as m:
            m.register_uri('POST', "{}/{}".format(self.session.base_url, endpoint), json=expected_return, status_code=200)
            response = self.session.request('post', endpoint)
            self.assertEqual(response, expected_return)

    def test_headers_initialization(self):
        headers_to_check = {
            k: v
            for k, v in iteritems(self.session.session.headers)
            if k in ['Authorization', 'X-Swiftype-Client', 'X-Swiftype-Client-Version']
        }
        version = elastic_app_search.__version__
        self.assertEqual(
            headers_to_check,
            {
                'Authorization': 'Bearer {}'.format(self.api_host_key),
                'X-Swiftype-Client': 'swiftype-app-search-python',
                'X-Swiftype-Client-Version': version
            }
        )

    def test_request_throw_error(self):
        endpoint = 'some_endpoint'

        with requests_mock.Mocker() as m:
            m.register_uri('POST', "{}/{}".format(self.session.base_url, endpoint), status_code=codes.unauthorized)

            with self.assertRaises(InvalidCredentials) as _context:
                self.session.request('post', endpoint)
