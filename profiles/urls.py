from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile, name="profile"),
    path("edit/", views.edit_profile, name="edit_profile"),

    path(
        "student/<int:student_id>/",
        views.student_profile,
        name="student_profile"
    ),
]