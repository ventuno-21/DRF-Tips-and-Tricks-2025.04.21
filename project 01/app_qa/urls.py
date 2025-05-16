from django.urls import path
from . import views


app_name = "home"
urlpatterns = [
    path("", views.QuestionListView.as_view()),
    path("create/", views.QuestionCreateView.as_view()),
    path("update/<int:pk>/", views.QuestionUpdateView.as_view()),
    path("delete/<int:pk>/", views.QuestionDeleteView.as_view()),
]
