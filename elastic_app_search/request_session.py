import requests
import elastic_app_search
from .exceptions import InvalidCredentials, NonExistentRecord, RecordAlreadyExists, BadRequest, Forbidden


class RequestSession:

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()

        headers = {
            'Authorization': "Bearer {}".format(api_key),
            'X-Swiftype-Client': 'elastic-app-search-python',
            'X-Swiftype-Client-Version': elastic_app_search.__version__,
            'content-type': 'application/json; charset=utf8'
        }
        self.session.headers.update(headers)

    def raise_if_error(self, response):
        if response.status_code == requests.codes.unauthorized:
            raise InvalidCredentials(response.reason)
        elif response.status_code == requests.codes.bad:
            raise BadRequest(response.text)
        elif response.status_code == requests.codes.conflict:
            raise RecordAlreadyExists()
        elif response.status_code == requests.codes.not_found:
            raise NonExistentRecord()
        elif response.status_code == requests.codes.forbidden:
            raise Forbidden()

        response.raise_for_status()

    def request(self, http_method, endpoint, base_url=None, **kwargs):
        return self.request_ignore_response(http_method, endpoint, base_url, **kwargs).json()

    def request_ignore_response(self, http_method, endpoint, base_url=None, **kwargs):
        base_url = base_url or self.base_url
        url = "{}/{}".format(base_url, endpoint)
        response = self.session.request(http_method, url, **kwargs)
        self.raise_if_error(response)
        return response
