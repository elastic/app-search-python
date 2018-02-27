from unittest import TestCase
import requests_mock

from swiftype_app_search import Client
from swiftype_app_search.exceptions import InvalidDocument

class TestClient(TestCase):

    def setUp(self):
        self.engine_name = 'engine_name'
        self.client = Client('account_host_key', 'api_key')

        self.document_index_url = "{}/{}".format(
            self.client.swiftype_session.base_url,
            "engines/{}/documents".format(self.engine_name)
        )

    def test_index_documents_validation(self):
        invalid_documents = [
            {
                'does': 'not have the id field'
            }
        ]
        with self.assertRaises(InvalidDocument) as context:
            self.client.index_documents('some engine name', invalid_documents)
        self.assertEqual(str(context.exception), 'Missing required fields: id')
        self.assertEqual(context.exception.document, invalid_documents[0])

    def test_index_documents(self):
        id = 'INscMGmhmX4'
        valid_document = {'id': id}
        expected_return = [
            {'id': id, 'errors': []}
        ]

        with requests_mock.Mocker() as m:
            m.register_uri('POST', self.document_index_url, json=expected_return, status_code=200)
            response = self.client.index_documents(self.engine_name, [valid_document])
            self.assertEqual(response, expected_return)

    def test_get_documents(self):
        id = 'INscMGmhmX4'
        expected_return = [
            {
                'id': id,
                'url': 'http://www.youtube.com/watch?v=v1uyQZNg2vE',
                'title': 'The Original Grumpy Cat',
                'body': 'this is a test'
            }
        ]

        with requests_mock.Mocker() as m:
            m.register_uri('GET', self.document_index_url, json=expected_return, status_code=200)
            response = self.client.get_documents(self.engine_name, [id])
            self.assertEqual(response, expected_return)

    def test_destroy_documents(self):
        id = 'INscMGmhmX4'
        expected_return = [
            {'id': id, 'result': True}
        ]

        with requests_mock.Mocker() as m:
            m.register_uri('DELETE', self.document_index_url, json=expected_return, status_code=200)
            response = self.client.destroy_documents(self.engine_name, [id])
            self.assertEqual(response, expected_return)

    def test_list_engines(self):
        expected_return = [
            { 'name': 'myawesomeengine' }
        ]

        with requests_mock.Mocker() as m:
            url = "{}/{}".format(self.client.swiftype_session.base_url, 'engines')
            m.register_uri('GET', url, json=expected_return, status_code=200)
            response = self.client.list_engines()
            self.assertEqual(response, expected_return)

    def test_get_engine(self):
        engine_name = 'myawesomeengine'
        expected_return = [
            { 'name': engine_name }
        ]

        with requests_mock.Mocker() as m:
            url = "{}/{}/{}".format(self.client.swiftype_session.base_url,
                                    'engines',
                                    engine_name)
            m.register_uri('GET', url, json=expected_return, status_code=200)
            response = self.client.get_engine(engine_name)
            self.assertEqual(response, expected_return)

    def test_create_engine(self):
        engine_name = 'myawesomeengine'
        expected_return = {'name': engine_name}

        with requests_mock.Mocker() as m:
            url = "{}/{}".format(self.client.swiftype_session.base_url, 'engines')
            m.register_uri('POST', url, json=expected_return, status_code=200)
            response = self.client.create_engine(engine_name)
            self.assertEqual(response, expected_return)

    def test_destroy_engine(self):
        engine_name = 'myawesomeengine'
        expected_return = {'deleted': True}

        with requests_mock.Mocker() as m:
            url = "{}/{}/{}".format(self.client.swiftype_session.base_url,
                                    'engines',
                                    engine_name)
            m.register_uri('DELETE', url, json=expected_return, status_code=200)
            response = self.client.destroy_engine(engine_name)
            self.assertEqual(response, expected_return)

    def test_search(self):
        query = 'query'

        with requests_mock.Mocker() as m:
            url = "{}/{}".format(
                self.client.swiftype_session.base_url,
                "engines/{}/search".format(self.engine_name)
            )
            m.register_uri('GET', url, json={}, status_code=200)
            self.client.search(self.engine_name, query, {})
