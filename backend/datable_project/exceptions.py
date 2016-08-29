from rest_framework.exceptions import APIException
from django.utils.encoding import force_text


class DatableBaseExceptions(APIException):
    status_code = 400
    default_detail = 'Unknown Error'

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = force_text(detail)
        else:
            self.detail = force_text(self.default_detail)


class SignUpRequiredFieldException(DatableBaseExceptions):
    status_code = 400
    default_detail = 'Unable to signup required fields(username,' \
                     'email, first_name, last_name, password'