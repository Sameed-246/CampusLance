from django.urls import path
from . import views


urlpatterns = [

    # All jobs
    path(
        "",
        views.job_list,
        name="job_list"
    ),

    # Post a job
    path(
        "post/",
        views.post_job,
        name="post_job"
    ),

    # View applicants
    path(
        "<int:job_id>/applicants/",
        views.view_applicants,
        name="view_applicants"
    ),

    # Scan an applicant's PDF resume against the job
    path(
        "application/<int:application_id>/scan-resume/",
        views.scan_applicant_resume,
        name="scan_applicant_resume"
    ),

    # Accept application
    path(
        "application/<int:application_id>/accept/",
        views.accept_application,
        name="accept_application"
    ),

    # Reject application
    path(
        "application/<int:application_id>/reject/",
        views.reject_application,
        name="reject_application"
    ),
]