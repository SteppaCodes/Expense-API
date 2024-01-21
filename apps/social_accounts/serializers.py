from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .utils import Google, register_social_user

class GoogleSignInSerializer(serializers.Serializer):
    access_token = serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        google_user_data = Google.validate(access_token)
        try:
            user_id = google_user_data['sub']
        except Exception as e:
            raise serializers.ValidationError(_("This token is invalid or has expired"))
        
        if google_user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed(detail=_("Could not validate user"))
        
        email = google_user_data['email']
        first_name = google_user_data['given_name']
        last_name= google_user_data['family_name']
        provider = "google"

        return register_social_user(provider, email, first_name, last_name)




