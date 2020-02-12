"""Exceptions raised by Elastic App Search Client."""

class ElasticAppSearchError(Exception):
    """Base class for all Elastic App Search errors."""

class InvalidCredentials(ElasticAppSearchError):
    """Raised when request cannot authenticate"""

class NonExistentRecord(ElasticAppSearchError):
    """Raised when record does not exist"""

class RecordAlreadyExists(ElasticAppSearchError):
    """Raised when record already exists"""

class BadRequest(ElasticAppSearchError):
    """Raised when bad request"""

    def __init__(self, message):
        super(ElasticAppSearchError, self).__init__(message)

class Forbidden(ElasticAppSearchError):
    """Raised when http forbidden"""

class SynchronousDocumentIndexingFailed(ElasticAppSearchError):
    """Raised when synchronous indexing of documents takes too long"""

class InvalidDocument(ElasticAppSearchError):
    """When a document has a non-accepted field or is missing a required field"""

    def __init__(self, message, document):
        super(ElasticAppSearchError, self).__init__(message)
        self.document = document
