from django.urls import path
from iotapp import views

urlpatterns = [
    path("", views.home, name="home"),
]