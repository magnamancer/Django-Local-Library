from django.urls import path
from . import views
from django.conf import settings

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
    path(
        "project_media/<str:media_type>/<int:pk>/",
        views.media_detail_view,
        name="media-detail",
    ),
    # path(
    #     "projects/<int:project_pk>/media/<int:media_pk>/",
    #     views.media_detail_view.as_view(),
    #     name="media-detail",
    # ),
]
