from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from backend.settings.settings import PRODUCTION

urlpatterns = (
    [
        path("intense_admin/", admin.site.urls),
        path("jet/", include("jet.urls", "jet")),  # Django JET URLS
        path(
            "jet/dashboard", include("jet.dashboard.urls", "jet-dashboard")
        ),  # Django JET URLS
        path("api/token/login/", TokenObtainPairView.as_view(), name="login"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
        path("api/token/verify/", TokenVerifyView.as_view(), name="verify"),
        path("api/", include("social_auth.api.urls", "social_auth")),
        path("api/", include("core.api.urls", "core")),
        path("api/", include("questions.api.urls", "questions")),
        path("api/", include("data.api.urls", "data")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

# If we are not in production, we want to see the API swagger and also the debug toolbar
# to check what is happening in the admin
if not PRODUCTION:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
        path("__debug__/", include("debug_toolbar.urls")),
    ]
