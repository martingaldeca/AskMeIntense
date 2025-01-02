from django.urls import path
from questions.api import views as questions_views

app_name = "questions"

urlpatterns = [
    path("categories/", questions_views.CategoryListView.as_view(), name="categories"),
    path("levels/", questions_views.LevelListView.as_view(), name="levels"),
    path("questions/", questions_views.QuestionListView.as_view(), name="questions"),
    path("random_question/<category>/<level>", questions_views.RandomQuestionGetView.as_view(), name="random_question"),
    path("questions/<uuid>/react/", questions_views.ReactToQuestionView.as_view(), name="question_react"),
    path(
        "questions/<uuid>/react/remove/", questions_views.RemoveReactionView.as_view(), name="question_remove_reaction"
    ),
]
