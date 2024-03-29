from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static
from .views import AutoRedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/", SpectacularSwaggerView.as_view(url_name="schema"), name="api"),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.expenses.urls")),
    path("api/", include("apps.user_stats.urls")),
    path("api/", include("apps.social_accounts.urls")),
    path("", AutoRedirectView.as_view()),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
