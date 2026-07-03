from rest_framework.exceptions import APIException


class AIServiceUnavailable(APIException):
  status_code = 503
  default_detail = "AI service is temporarily unavailable."
  default_code = 'ai_service_unavailable'


class AIInvalidResponse(APIException):
  status_code = 502
  default_detail = 'OpenAI returned invalid JSON'
  default_code = 'invalid_json'
