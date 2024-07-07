from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = 400
    default_detail = '존재하지 않는 사용자입니다.'


class UserPasswordNotMatchException(APIException):
    status_code = 400
    default_detail = '비밀번호가 일치하지 않습니다.'


class UserAlreadyExistsException(APIException):
    status_code = 400
    default_detail = '이미 존재하는 사용자입니다.'


class PostNotFoundException(APIException):
    status_code = 400
    default_detail = '존재하지 않는 게시글입니다.'


class PostPermissionDeniedException(APIException):
    status_code = 400
    default_detail = '게시글 작성자만 수정, 삭제가 가능합니다.'
