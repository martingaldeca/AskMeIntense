from core.api import views as core_views
from django.urls import path

app_name = "core"

urlpatterns = [
    path("register/", core_views.RegisterView.as_view(), name="register"),
    path("me/", core_views.MeDetailView.as_view(), name="me"),
]
