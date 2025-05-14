from .views import PersonRegister
from django.urls import path

urlpatterns = [
    path("register/", PersonRegister.as_view()),
]
