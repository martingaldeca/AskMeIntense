from django.urls import path
from questions.api import views as questions_views

app_name = "questions"

urlpatterns = [
    path("categories/", questions_views.CategoryListView.as_view(), name="categories"),
    path("levels/", questions_views.LevelListView.as_view(), name="levels"),
    path("questions/", questions_views.QuestionListView.as_view(), name="questions"),
]
