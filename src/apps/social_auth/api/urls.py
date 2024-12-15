from django.urls import path
from social_auth.api import views as social_auth_views

app_name = "social_auth"

urlpatterns = [
    path(
        "token/google/",
        social_auth_views.GoogleSocialAuthView.as_view(),
        name="google_auth",
    ),
]
