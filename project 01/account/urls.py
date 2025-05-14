from django.urls import path

from .views import PersonRegister, PersonRegister2

urlpatterns = [
    path("register/", PersonRegister.as_view()),
    path("register2/", PersonRegister2.as_view()),
]
