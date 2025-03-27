from data.api import views as data_views
from django.urls import path

app_name = "data"

urlpatterns = [
    path("data_event/", data_views.DataEventView.as_view(), name="data-event"),
]
