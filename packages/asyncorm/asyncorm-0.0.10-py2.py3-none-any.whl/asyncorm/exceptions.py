__all__ = ('FieldError', 'ManagerError', 'ModelError', 'ModuleError',
           'QuerysetError', 'SerializerError')


class AsyncormException(Exception):
    pass


class FieldError(AsyncormException):
    '''to be raised when there are field errors detected'''
    pass


class ManagerError(AsyncormException):
    '''to be raised when there are queryset errors detected'''
    pass


class ModelError(AsyncormException):
    '''to be raised when there are model errors detected'''
    pass


class SerializerError(AsyncormException):
    '''to be raised when there are model errors detected'''
    pass


class ModuleError(AsyncormException):
    '''to be raised when there are model module or config errors detected'''
    pass


class QuerysetError(AsyncormException):
    '''to be raised when there are queryset errors detected'''
    pass
