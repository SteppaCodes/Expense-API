
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.accounts.urls')),
    path('api/', include('apps.expenses.urls')),
    path('api/', include('apps.user_stats.urls')),
    path('api/', include('apps.social_accounts.urls')),
]


handle_404 = 'utils.views.error_404'
handle_500 = 'utils.views.error_500'