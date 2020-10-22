from django.urls import path
from . import views

app_name = "mainpage"
urlpatterns = [
    path(r"", views.home, name="home"),
    path(r"textbook", views.choose_textbook, name="textbook"),
    path(r"test/<str:filename>/", views.get_test, name="test"),
]

