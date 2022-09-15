from rest_framework.views import exception_handler
# from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # print(response, exc)

    if response is not None and response.status_code==400:
        response.data = {"code": 400, "message": "Validation Failed"}

    return response