from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # Testing Landing, generic, elements
    path("landing/", views.landing, name="landing"),
    path("generic/", views.generic, name="generic"),
    path("elements/", views.elements, name="elements"),
    path("resume/", views.resume, name="resume"),
    path("projects/", views.projects_page, name="projects"),
    path(
        "projects/<int:pk>",
        views.project_detail_view.as_view(),
        name="project-detail",
    ),
]
