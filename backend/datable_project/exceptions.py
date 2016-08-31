from rest_framework.exceptions import APIException
from django.utils.encoding import force_text


class DatableBaseExceptions(APIException):
    default_detail = 'Unknown Error'

    def __init__(self, detail=None, status_code=400):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)
        self.status_code = status_code


class SignUpRequiredFieldException(DatableBaseExceptions):
    default_detail = 'Unable to signup required fields(username,' \
                     'email, first_name, last_name, password'


class VerifyTokenKeyError(DatableBaseExceptions):
    default_detail = 'provider, access_token are required'


class GoogleBadTokenError(DatableBaseExceptions):
    default_detail = 'google token cannot be verified'


class BadTokenError(DatableBaseExceptions):
    default_detail = 'token cannot be verified'


class NotImplementedEXception(DatableBaseExceptions):
    default_detail = 'Not Implemented Exception'


class UnAuthorizedError(DatableBaseExceptions):
    status_code = 401
    default_detail = 'Unable to login'
