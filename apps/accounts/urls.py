from django.urls import path 
from . views import (
    RegisterView, VerifyEmailView,
    LoginUserView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-email/<token>', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view()),
]