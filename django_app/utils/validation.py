import requests

from config import settings
from utils import customexception

__all__ = (
    'CheckSocialAccessToken',
    'ImageValidate'
)


class CheckSocialAccessToken():
    def check_facebook(access_token):
        url = 'https://graph.facebook.com/debug_token'
        param = {
            'input_token': access_token,
            'access_token': settings.CONFIG_FILE['facebook']['app-access-token']
        }
        response = requests.get(url, params=param)
        response_dict = response.json()
        is_valid = response_dict['data']['is_valid']
        if is_valid:
            pass
        else:
            raise customexception.AuthenticateException('Invalid Access Token')
        return is_valid

    def check_google(access_token):
        url = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
        params = {
            'access_token': access_token
        }
        response = requests.get(url, params=params)
        response_dict = response.json()
        print(response_dict)
        print(settings.CONFIG_FILE['google']['client-id'].values())
        if 'aud' in response_dict.keys():
            if response_dict['aud'] in settings.CONFIG_FILE['google']['client-id'].values():
                return True
            else:
                raise customexception.AuthenticateException('Invalid Access Token')
        else:
            raise customexception.AuthenticateException('Invalid Access Token')


class ImageValidate():
    def imagevalidate(file):
        filename = file.name
        filesize = file.size
        print(filesize)
        print(type(filesize))
        VALID_EXTENSION = [
            'jpg',
            'png'
        ]
        VALID_FILESIZE = 5242880
        print(VALID_FILESIZE)
        if filesize > VALID_FILESIZE:
            raise customexception.ValidationException('Image size must be less than 5MB.')
        else:
            try:
                name, extention = filename.split('.')
                if extention.lower() in VALID_EXTENSION:
                    return True
                else:
                    return False
            except:
                raise customexception.ValidationException("It's not valid Extension")
