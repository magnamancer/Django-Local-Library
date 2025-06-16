from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Testing Landing,
    path("landing/", views.landing, name="landing"),
    path("generic/", views.generic, name="generic"),
    path("elements/", views.elements, name="elements"),
]
