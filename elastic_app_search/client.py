import json
import jwt
from .request_session import RequestSession
from .exceptions import InvalidDocument


class Client:

    ELASTIC_APP_SEARCH_BASE_ENDPOINT = 'api.swiftype.com/api/as/v1'
    SIGNED_SEARCH_TOKEN_JWT_ALGORITHM = 'HS256'

    def __init__(self, host_identifier='', api_key='',
                 base_endpoint=ELASTIC_APP_SEARCH_BASE_ENDPOINT,
                 use_https=True,
                 account_host_key='' # Deprecated - use host_identifier instead
                 ):
        self.host_identifier = host_identifier or account_host_key
        self.account_host_key = self.host_identifier # Deprecated
        self.api_key = api_key

        uri_scheme = 'https' if use_https else 'http'
        host_prefix = host_identifier + '.' if host_identifier else ''
        base_url = "{}://{}{}".format(uri_scheme, host_prefix, base_endpoint)
        self.session = RequestSession(self.api_key, base_url)

    def get_documents(self, engine_name, document_ids):
        """
        Retrieves documents by id from an engine.

        :param engine_name: Name of engine to get documents from.
        :param document_ids: Ids of documents to be returned.
        :return: Array of dictionaries representing documents.
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(document_ids)
        return self.session.request('get', endpoint, data=data)

    def list_documents(self, engine_name, current=1, size=20):
        """
        Lists all documents in engine.

        :param current: Page of documents
        :param size: Number of documents to return per page
        :return: List of documemts.
        """
        data = { 'page': { 'current': current, 'size': size } }
        return self.session.request('get', "engines/{}/documents/list".format(engine_name), json=data)

    def index_document(self, engine_name, document):
        """
        Create or update a document for an engine. Raises
        :class:`~elastic_app_search.exceptions.InvalidDocument` when the document
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

        return self.session.request('post', endpoint, data=data)

    def update_documents(self, engine_name, documents):
        """
        Update a batch of documents for an engine.

        :param engine_name: Name of engine to index documents into.
        :param documents: Hashes representing documents.
        :return: Array of document status dictionaries. Errors will be present
        in a document status with a key of `errors`.
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(documents)

        return self.session.request('patch', endpoint, data=data)

    def destroy_documents(self, engine_name, document_ids):
        """
        Destroys documents by id for an engine.

        :param engine_name: Name of engine.
        :param document_ids: Array of document ids of documents to be destroyed.
        :return:
        """
        endpoint = "engines/{}/documents".format(engine_name)
        data = json.dumps(document_ids)
        return self.session.request('delete', endpoint, data=data)

    def get_schema(self, engine_name):
        """
        Get current schema for an engine.

        :param engine_name: Name of engine.
        :return: Schema.
        """
        endpoint = "engines/{}/schema".format(engine_name)
        return self.session.request('get', endpoint)

    def update_schema(self, engine_name, schema):
        """
        Create new schema fields or update the fields if they already exists.

        :param engine_name: Name of engine.
        :param schema: Schema to be updated as dict.
        :return: Updated schema.
        """
        endpoint = "engines/{}/schema".format(engine_name)
        data = json.dumps(schema)
        return self.session.request('post', endpoint, data=data)

    def list_engines(self, current=1, size=20):
        """
        Lists engines that the api key has access to.

        :param current: Page of engines
        :param size: Number of engines to return per page
        :return: List of dictionaries with key value pair corresponding to the
        name of the engine.
        """
        data = { 'page': { 'current': current, 'size': size } }
        return self.session.request('get', 'engines', json=data)

    def get_engine(self, engine_name):
        """
        Retrieves an engine by name.
        :param engine_name: Name of an existing engine.
        :return: A dictionary corresponding to the name of the engine.
        """
        return self.session.request('get', "engines/{}".format(engine_name))

    def create_engine(self, engine_name, language=None, options=None):
        """
        Creates an engine with the specified name.
        :param engine_name: Name of the new engine.
        :param language: Language of the new engine.
        :param options: Engine configuration.
        :return: A dictionary corresponding to the new engine.
        """
        data = { 'name': engine_name }
        if language is not None:
            data['language'] = language
        if options is not None:
            data.update(options)
        return self.session.request('post', 'engines', json=data)

    def destroy_engine(self, engine_name):
        """
        Destroys an engine by name.
        :param engine_name: Name of an existing engine.
        :return: A dictionary with a single key of `deleted` and a value of
        True or False.
        """
        return self.session.request('delete', "engines/{}".format(engine_name))

    def list_synonym_sets(self, engine_name, current=1, size=20):
        """
        Lists all synonym sets in engine.

        :param engine_name: Name of the engine.
        :param current: Page of synonym sets.
        :param size: Number of synonym sets to return per page.
        :return: List of synonym sets.
        """
        data = { 'page': { 'current': current, 'size': size } }
        return self.session.request('get', "engines/{}/synonyms".format(engine_name), json=data)

    def get_synonym_set(self, engine_name, synonym_set_id):
        """
        Get a single synonym set.

        :param engine_name: Name of the engine.
        :param synonym_set_id: ID of the synonym set.
        :return: A single synonym set.
        """
        return self.session.request('get', "engines/{}/synonyms/{}".format(engine_name, synonym_set_id))

    def create_synonym_set(self, engine_name, synonyms):
        """
        Create a synonym set.

        :param engine_name: Name of the engine.
        :param synonyms: List of synonyms.
        :return: A list of synonyms that was created.
        """
        data = { 'synonyms': synonyms }
        return self.session.request('post', "engines/{}/synonyms".format(engine_name), json=data)

    def update_synonym_set(self, engine_name, synonym_set_id, synonyms):
        """
        Update an existing synonym set.

        :param engine_name: Name of the engine.
        :param synonym_set_id: ID of the synonym set to update.
        :param synonyms: The updated list of synonyms.
        :return: The synonym set that was updated.
        """
        data = { 'synonyms': synonyms }
        return self.session.request('put', "engines/{}/synonyms/{}".format(engine_name, synonym_set_id), json=data)

    def destroy_synonym_set(self, engine_name, synonym_set_id):
        """
        Destroy a synonym set.

        :param engine_name: Name of the engine.
        :param synonym_set_id: ID of the synonym set to be deleted.
        :return: Delete status.
        """
        return self.session.request('delete', "engines/{}/synonyms/{}".format(engine_name, synonym_set_id))

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
        return self.session.request('get', endpoint, json=options)

    def multi_search(self, engine_name, searches=None):
        """
        Run multiple searches for documents on a single request.
        See https://swiftype.com/documentation/app-search/ for more details
        on options and return values.

        :param engine_name: Name of engine to search over.
        :param options: Array of search options. ex. {query: String, options: Dict}
        """

        def build_options_from_search(search):
            if 'options' in search:
                options = search['options']
            else:
                options = {}
            options['query'] = search['query']
            return options

        endpoint = "engines/{}/multi_search".format(engine_name)
        options = {
            'queries': list(map(build_options_from_search, searches))
        }
        return self.session.request('get', endpoint, json=options)

    def query_suggestion(self, engine_name, query, options=None):
        """
        Request Query Suggestions. See https://swiftype.com/documentation/app-search/ for more details
        on options and return values.

        :param engine_name: Name of engine to search over.
        :param query: Query string to search for.
        :param options: Dict of search options.
        """
        endpoint = "engines/{}/query_suggestion".format(engine_name)
        options = options or {}
        options['query'] = query
        return self.session.request('get', endpoint, json=options)

    def click(self, engine_name, options):
        """
        Sends a click event to the Elastic App Search Api, to track a click-through event.
        See https://swiftype.com/documentation/app-search/ for more details
        on options and return values.

        :param engine_name: Name of engine to search over.
        :param options: Dict of search options.
        """
        endpoint = "engines/{}/click".format(engine_name)
        return self.session.request_ignore_response('post', endpoint, json=options)

    def create_meta_engine(self, engine_name, source_engines):
        data = {
            'name': engine_name,
            'source_engines': source_engines,
            'type': 'meta'
        }
        return self.session.request('post', 'engines', json=data)

    def add_meta_engine_sources(self, engine_name, source_engines):
        endpoint = "engines/{}/source_engines".format(engine_name)
        return self.session.request('post', endpoint, json=source_engines)

    def delete_meta_engine_sources(self, engine_name, source_engines):
        endpoint = "engines/{}/source_engines".format(engine_name)
        return self.session.request('delete', endpoint, json=source_engines)

    def get_search_settings(self, engine_name):
        """
        Get search settings for an engine.

        :param engine_name: Name of the engine.
        """
        endpoint = "engines/{}/search_settings".format(engine_name)
        return self.session.request('get', endpoint)

    def update_search_settings(self, engine_name, search_settings):
        """
        Update search settings for an engine.

        :param engine_name: Name of the engine.
        :param search_settings: New search settings JSON
        """
        endpoint = "engines/{}/search_settings".format(engine_name)
        return self.session.request('put', endpoint, json=search_settings)

    def reset_search_settings(self, engine_name):
        """
        Reset search settings to default for the given engine.

        :param engine_name: Name of the engine.
        """
        endpoint = "engines/{}/search_settings/reset".format(engine_name)
        return self.session.request('post', endpoint)

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

    def get_api_logs(self, engine_name, options=None):
        """
        Searches the API logs.

        :param engine_name: Name of engine.
        :param options: Dict of search options.
        """
        endpoint = "engines/{}/logs/api".format(engine_name)
        options = options or {}
        return self.session.request('get', endpoint, json=options)

