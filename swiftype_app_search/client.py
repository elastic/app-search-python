import json
import jwt
from .swiftype_request_session import SwiftypeRequestSession
from .exceptions import InvalidDocument


class Client:

    SWIFTYPE_APP_SEARCH_BASE_ENDPOINT = 'api.swiftype.com/api/as/v1'
    SIGNED_SEARCH_TOKEN_JWT_ALGORITHM = 'HS256'

    def __init__(self, account_host_key, api_key,
                 base_endpoint=SWIFTYPE_APP_SEARCH_BASE_ENDPOINT,
                 use_https=True):
        self.account_host_key = account_host_key
        self.api_key = api_key

        uri_scheme = 'https' if use_https else 'http'
        base_url = "{}://{}.{}".format(uri_scheme, account_host_key, base_endpoint)
        self.swiftype_session = SwiftypeRequestSession(self.api_key, base_url)

    def get_documents(self, engine_name, document_ids):
        """
        Retrieves documents by id from an engine.

        :param engine_name: Name of engine to get documents from.
        :param document_ids: Ids of documents to be returned.
        :return: Array of dictionaries representing documents.
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(document_ids)
        return self.swiftype_session.request('get', endpoint, data=data)

    def index_document(self, engine_name, document):
        """
        Create or update a document for an engine. Raises
        :class:`~swiftype_app_search.exceptions.InvalidDocument` when the document
        has processing errors

        :param engine_name: Name of engine to index documents into.
        :param document: Hash representing a single document.
        :return: dict processed document status
        """
        document_status = self.index_documents(engine_name, [document])[0]
        errors = document_status['errors']
        if errors:
            raise InvalidDocument('; '.join(errors), document)

        return {
            key: document_status[key]
            for key in document_status
            if key != 'errors'
        }

    def index_documents(self, engine_name, documents):
        """
        Create or update documents for an engine.

        :param engine_name: Name of engine to index documents into.
        :param documents: Hashes representing documents.
        :return: Array of document status dictionaries. Errors will be present
        in a document status with a key of `errors`.
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(documents)

        return self.swiftype_session.request('post', endpoint, data=data)

    def destroy_documents(self, engine_name, document_ids):
        """
        Destroys documents by id for an engine.

        :param engine_name: Name of engine.
        :param document_ids: Array of document ids of documents to be destroyed.
        :return:
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(document_ids)
        return self.swiftype_session.request('delete', endpoint, data=data)

    def list_engines(self, current=1, size=20):
        """
        Lists engines that the api key has access to.

        :param current: Page of engines
        :param size: Number of engines to return per page
        :return: List of dictionaries with key value pair corresponding to the
        name of the engine.
        """
        data = { 'page': { 'current': current, 'size': size } }
        return self.swiftype_session.request('get', 'engines', json=data)

    def get_engine(self, engine_name):
        """
        Retrieves an engine by name.
        :param engine_name: Name of an existing engine.
        :return: A dictionary corresponding to the name of the engine.
        """
        return self.swiftype_session.request('get', "engines/{}".format(engine_name))

    def create_engine(self, engine_name):
        """
        Creates an engine with the specified name.
        :param engine_name: Name of the new engine.
        :return: A dictionary corresponding to the name of the engine.
        """
        data = { 'name': engine_name }
        return self.swiftype_session.request('post', 'engines', json=data)

    def destroy_engine(self, engine_name):
        """
        Destroys an engine by name.
        :param engine_name: Name of an existing engine.
        :return: A dictionary with a single key of `deleted` and a value of
        True or False.
        """
        return self.swiftype_session.request('delete', "engines/{}".format(engine_name))

    def search(self, engine_name, query, options=None):
        """
        Search an engine. See https://swiftype.com/documentation/app-search/ for more details
        on options and return values.

        :param engine_name: Name of engine to search over.
        :param query: Query string to search for.
        :param options: Dict of search options.
        """
        endpoint = "engines/{}/search".format(engine_name)
        options = options or {}
        options['query'] = query
        return self.swiftype_session.request('get', endpoint, json=options)

    @staticmethod
    def create_signed_search_key(api_key, api_key_name, options):
        """
        Creates a signed API key that will overwrite all search options (except
        filters) made with this key.

        :param api_key: An API key to use for this client.
        :param api_key_name: The unique name for the API Key
        :param options: Search options to override.
        :return: A JWT signed api token.
        """
        options['api_key_name'] = api_key_name
        return jwt.encode(options, api_key, algorithm=Client.SIGNED_SEARCH_TOKEN_JWT_ALGORITHM)
