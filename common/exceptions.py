import json


class BadRequest(Exception):
    """Bad Request Exception (400)"""
    def __str__(self):
        return 'Bad Request'


class AuthenticationException(Exception):
    """Unauthenticated Exception (401)"""
    def __str__(self):
        return 'Unauthenticated'


class FormErrorBag:
    def __init__(self, errors: list):
        self.errors = errors

    def has(self, key):
        return key in self.errors

    def get(self, key=None, default=None):
        if key is None:
            return self.errors

        if self.has(key):
            error = self.errors[key]
            if isinstance(error, list):
                return error[0] if len(error) > 0 else None
            else:
                return error

        return default

    def serialize(self):
        return json.dumps(self.errors)

    def __repr__(self):
        return self.serialize()

    @staticmethod
    def dumper(obj):
        if "serialize" in dir(obj):
            return obj.serialize()

        return obj.errors
