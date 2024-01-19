from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from .models import User

from rest_framework.validators import ValidationError

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

    

class SendMail:

    @staticmethod
    def verification(request, email, *args, **Kwargs):
        user = User.objects.get(email=email)
        tokens = user.tokens()
        access_token = tokens.get('access')
        subject = 'Email Verification'
        domain = get_current_site(request).domain
        relative_url = reverse('verify-email',kwargs={'token':access_token})
        abs_url = f"http://{domain}{relative_url}"
        # 'access_token':str(tokens.get('access')),
        #'refresh_token':str(tokens.get('refresh'))

        message = EmailMessage(
                subject=subject, 
                body=f"Hi {user.full_name}, please click the link to activate your email \n{abs_url}",
                to = [user.email]
        )
        message.content_subtype = "html"

        EmailThread(message).start()


    @staticmethod
    def resetpassword(request, email):
        try:
            user = User.objects.get(email=email)
            subject = "Reset Password"
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = token = PasswordResetTokenGenerator().make_token(user)
            domain = get_current_site(request).domain
            relative_url = reverse("password-reset-confirm", 
                                   kwargs={'uidb64': uidb64, "token":token})
            abs_url = f"http://{domain}{relative_url}"

            message = EmailMessage(
                subject=subject, 
                body = f"Link to reset your password\n{abs_url}",
                to= [user.email]
            )

            # message.content_subtype('html')
            EmailThread(message).start()

        except User.DoesNotExist:
            raise ValidationError(_(f"User with the email {email} does not exist"))

