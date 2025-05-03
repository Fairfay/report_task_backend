from rest_framework.exceptions import APIException
from rest_framework import status


class InternalServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Внутренняя ошибка сервера.'
    default_code = 'internal_server_error'