import requests

from config import settings
from utils import customexception

__all__ = (
    'CheckSocialAccessToken',
    'ImageValidate'
)


class CheckSocialAccessToken():
    def check_facebook(access_token):
        param = {
            'input_token': access_token,
            'access_token': settings.CONFIG_FILE['facebook']['app-access-token']
        }
        response = requests.get('https://graph.facebook.com/debug_token', params=param)
        response_dict = response.json()
        is_valid = response_dict['data']['is_valid']
        if is_valid:
            pass
        else:
            raise customexception.AuthenticateException('Invalid Access Token')
        return is_valid


class ImageValidate():
    def imagevalidate(filename):
        VALID_EXTENSION = [
            'jpg',
            'png'
        ]
        try:
            name, extention = filename.split('.')
            if extention.lower() in VALID_EXTENSION:
                return True
            else:
                return False
        except:
            raise customexception.ValidationException("It's not valid Extension")
