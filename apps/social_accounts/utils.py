from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth import authenticate
from django.conf import settings 

from apps.accounts.models import User


class Google:
    @staticmethod
    def validate(self, access_token):
        """
        Validate the given access token from google.
        """
        try:
            id_info = id_token.verify_oauth2_token(access_token, requests.Request)
            #Check if google is the site where the token is from
            if "accounts.google.con" in id_info['iss']:
                return id_info
        except Exception as e:
            return "Token is invalid"


def login_social_user(email, password):
    user = authenticate(email=email, password=password)
    user_tokens = user.tokens()
    return {
        'email': user.email,
        'access_token': str(user_tokens['access']),
        'refresh_token': str(user_tokens['refresh'])
        }

def register_social_user(provider, email, first_name, last_name):
    user = User.objects.get(email=email)
    password = settings.SOCIAL_AUTH_PASSWORD
    if user:
        #check if the user provider is google which means the use signed up usig google
        if provider == user.auth_provider:
           result = login_social_user(email, password)
           return result
        else:
            raise AuthenticationFailed(
                detail = f"Please continue your login with {user.auth_provider}"
            )
    else:
        new_user = {
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":password
        }
        #create the user 
        register_user = User.objects.create_user(**new_user)
        register_user.auth_provider = provider
        register_user.is_email_verified = True
        register_user.save()
        #login the user
        result = login_social_user(email, password)
        return result

