from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
import threading

from .models import User


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send()

    

class Sendmail:

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
