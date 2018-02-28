"""Class of invalid usage."""


class InvalidUsage(Exception):
    """Class of invalid usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Init class."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert class to dict."""
        result = dict(self.payload or ())
        result['message'] = self.message
        result['status_code'] = self.status_code
        return result
