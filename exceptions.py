class SQLConnectionError(BaseException):
    value: any


class SQLQueryError(BaseException):
    value: any
