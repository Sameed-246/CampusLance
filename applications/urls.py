from django.urls import path
from . import views


urlpatterns = [

    path(
        "apply/<int:job_id>/",
        views.apply_job,
        name="apply_job"
    ),

    path(
        "my/",
        views.my_applications,
        name="my_applications"
    ),

    path(
        "<int:application_id>/",
        views.application_detail,
        name="application_detail"
    ),

    path(
        "accept/<int:application_id>/",
        views.accept_application,
        name="accept_application"
    ),

    path(
        "reject/<int:application_id>/",
        views.reject_application,
        name="reject_application"
    ),

]