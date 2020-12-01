import requests

from urllib.parse import urlencode

from django.urls import reverse
from oauth2_provider.models import Grant, RefreshToken
from rest_framework import status

from .models import MyApplication

_BASE_API_PATH = 'http://127.0.0.1:8000/oauth'


def revoke_token(request, app_id):
    application_object = MyApplication.objects.get(pk=app_id)

    url = f"{_BASE_API_PATH}/revoke_token/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    access_token = request.user.oauth2_provider_accesstoken.get(application_id=app_id).token
    data = {
        "client_id": application_object.client_id,
        "client_secret": application_object.client_secret(application_object),
        "token": access_token
    }
    response = requests.post(url, headers=headers, data=data)

    if response.ok:
        request.user.oauth2_provider_refreshtoken.get(application_id=app_id).delete()

    return {"detail": "Access token was revoked"}


def request_to_get_access_token(request):
    authorization_code = request.GET['code']
    application_to_authorize = Grant.objects.get(code=authorization_code).application
    client_id = application_to_authorize.client_id
    client_secret = application_to_authorize.client_secret
    redirect_uri = request.build_absolute_uri().split('/?')[0]

    url = f"{_BASE_API_PATH}/token/"
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    response = requests.post(url, headers=headers, data=data)
    return response


def request_to_refresh_access_token(request):
    client_id = request.POST.get("client_id", None)
    refresh_token = request.POST.get("refresh_token", None)
    error_message = {}

    try:
        app_obj = MyApplication.objects.get(client_id=client_id)
        refresh_token_obj = RefreshToken.objects.get(token=refresh_token, application__pk=app_obj.id)
    except MyApplication.DoesNotExist:
        error_message = {
            "detail": f"client_id isn't correct"
        }
    except RefreshToken.DoesNotExist:
        if RefreshToken.objects.filter(token=refresh_token):
            error_message = {
                "detail": "client_id isn't correct"
            }
        else:
            error_message = {
                "detail": "refresh_token isn't correct"
            }

    if error_message:
        error_info = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "data": error_message
        }
        return error_info

    client_secret = app_obj.client_secret
    url = f"{_BASE_API_PATH}/token/"
    data = {
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
    }
    response = requests.post(url, data=data)

    if response.ok:
        refresh_token_obj.delete()
        response.status_code = status.HTTP_201_CREATED

    response_info = {
        "status_code": response.status_code,
        "data": response.json()
    }
    return response_info


def get_redirect_url(request, client_id):
    """Create url for oauth authorization"""
    try:
        app_obj = MyApplication.objects.get(client_id=client_id)
    except MyApplication.DoesNotExist:
        return reverse("login")
    scopes = ' '.join(app_obj.scope.choices[elem] for elem in app_obj.scope)
    url_args = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scopes,
        "redirect_uri": "http://127.0.0.1:8000/noexist/callback"
    }
    return f'{_BASE_API_PATH}/authorize/?{urlencode(url_args, safe="://")}'


def authorize_user_by_request(request):
    """Make request to get session from server service/"""
    url = "http://192.168.32.89:8000/Auth"

    # credentials = {
    #     'username': request.POST["username"],
    #     'password': request.POST["password"]
    # }

    credentials = {
        'username': 'nikita',
        'password': 'nikita'
    }

    s = requests.Session()
    s.post(url, data=credentials)
    return s


def get_user_data(request):
    s = authorize_user_by_request(request)
    url = "http://192.168.32.89:8000/GetPerson"
    response = s.get(url)
    return response.json()