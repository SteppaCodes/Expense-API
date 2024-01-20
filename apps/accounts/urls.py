from django.urls import path 
from . views import (
    RegisterView, VerifyEmailView,
    LoginUserView, SetNewPassword, PasswordResetConfirm, ResetPasswordRequest
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<token>', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('set-new-password/', SetNewPassword.as_view()),
    path('password-reset-confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('reset-password-request/', ResetPasswordRequest.as_view()),
]