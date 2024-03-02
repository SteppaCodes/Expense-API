from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/', SpectacularSwaggerView.as_view(url_name="schema")),

    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.expenses.urls")),
    path("api/", include("apps.user_stats.urls")),
    path("api/", include("apps.social_accounts.urls")),
]


handle_404 = "utils.views.error_404"
handle_500 = "utils.views.error_500"
