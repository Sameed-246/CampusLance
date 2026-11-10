
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Application
from jobs.models import Job


# ============================================================
# APPLY FOR JOB
# ============================================================

@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    # Only students can apply
    if getattr(request.user, "role", None) != "student":

        return redirect("job_list")

    # Prevent students from applying to their own job
    if job.client == request.user:

        return redirect("job_list")

    # Prevent duplicate applications
    existing_application = Application.objects.filter(
        job=job,
        student=request.user
    ).first()

    if existing_application:

        return redirect("student_dashboard")

    # Submit application
    if request.method == "POST":

        proposal = request.POST.get(
            "proposal",
            ""
        ).strip()

        if proposal:

            Application.objects.create(
                job=job,
                student=request.user,
                proposal=proposal,
                status="Pending"
            )

            return redirect("student_dashboard")

    # Show application form
    return render(
        request,
        "applications/apply_job.html",
        {
            "job": job
        }
    )


# ============================================================
# ACCEPT APPLICATION
# ============================================================

@login_required
def accept_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    # Only the job owner/client can accept
    if application.job.client != request.user:

        return redirect("client_dashboard")

    application.status = "Accepted"

    application.save()

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# ============================================================
# REJECT APPLICATION
# ============================================================

@login_required
def reject_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    # Only the job owner/client can reject
    if application.job.client != request.user:

        return redirect("client_dashboard")

    application.status = "Rejected"

    application.save()

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )


# ============================================================
# APPLICATION DETAIL
# ============================================================

@login_required
def application_detail(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        student=request.user
    )

    return render(
        request,
        "applications/application_detail.html",
        {
            "application": application
        }
    )


# ============================================================
# MY APPLICATIONS
# ============================================================

@login_required
def my_applications(request):

    applications = Application.objects.filter(
        student=request.user
    ).select_related(
        "job"
    ).order_by(
        "-applied_at"
    )

    return render(
        request,
        "applications/my_applications.html",
        {
            "applications": applications,
        }
    )

