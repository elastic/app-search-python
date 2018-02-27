"""Exceptions raised by Swiftype App Search Client."""

class SwiftypeAppSearchError(Exception):
    """Base class for all Swiftype App Search errors."""

class InvalidCredentials(SwiftypeAppSearchError):
    """Raised when request cannot authenticate"""

class NonExistentRecord(SwiftypeAppSearchError):
    """Raised when record does not exist"""

class RecordAlreadyExists(SwiftypeAppSearchError):
    """Raised when record already exists"""

class BadRequest(SwiftypeAppSearchError):
    """Raised when bad request"""

class Forbidden(SwiftypeAppSearchError):
    """Raised when http forbidden"""

class SynchronousDocumentIndexingFailed(SwiftypeAppSearchError):
    """Raised when synchronous indexing of documents takes too long"""

class InvalidDocument(SwiftypeAppSearchError):
    """When a document has a non-accepted field or is missing a required field"""

    def __init__(self, message, document):
        super(SwiftypeAppSearchError, self).__init__(message)
        self.document = document
