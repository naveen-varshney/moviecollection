class BaseException(Exception):
    pass


class ResponseException(BaseException):
    pass


class ApiTimeoutException(BaseException):
    pass


class ApiConnectionErrorException(BaseException):
    pass
