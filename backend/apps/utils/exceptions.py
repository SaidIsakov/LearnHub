from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


STATUS_CODE_MAP = {
    400: 'validation_error',
    401: 'unauthorized',
    403: 'permission_denied',
    404: 'not_found',
    500: 'internal_server_error',
}


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)

  if response is not None:
    original_data = response.data


    response.data = {
      'error': {
        'code': STATUS_CODE_MAP.get(response.status_code, 'unknown_error'),
        'message': original_data.get('detail'),
        'details': original_data
      }
    }


  return response
