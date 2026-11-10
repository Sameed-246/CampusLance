from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models
from pypdf.errors import PdfReadError, PdfStreamError

from .models import Job
from .forms import JobForm

from applications.models import Application
from profiles.models import StudentProfile
from messaging.models import Message
from .resume_scanner import (
    MAX_RESUME_FILE_SIZE,
    analyze_resume,
    extract_resume_text,
)


def _applicants_context(job):
    applications = (
        Application.objects
        .filter(job=job)
        .select_related("student")
        .order_by("-applied_at")
    )

    for application in applications:
        application.student_profile, _ = StudentProfile.objects.get_or_create(
            user=application.student
        )

    return {
        "job": job,
        "applications": applications,
    }

# ============================================================
# JOB LIST
# ============================================================

@login_required
def job_list(request):

    jobs = Job.objects.all()

    # Search
    search = request.GET.get("search", "").strip()

    if search:
        jobs = jobs.filter(
            models.Q(title__icontains=search)
            | models.Q(description__icontains=search)
            | models.Q(category__icontains=search)
        )

    # Category filter
    category = request.GET.get("category", "").strip()

    if category:
        jobs = jobs.filter(category=category)

    # Sorting
    sort = request.GET.get("sort", "newest")

    if sort == "oldest":
        jobs = jobs.order_by("created_at")

    elif sort == "budget_high":
        jobs = jobs.order_by("-budget")

    elif sort == "budget_low":
        jobs = jobs.order_by("budget")

    else:
        jobs = jobs.order_by("-created_at")

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "search": search,
            "selected_category": category,
            "selected_sort": sort,
            "categories": Job.CATEGORY_CHOICES,
        }
    )

# ============================================================
# POST JOB
# ============================================================

@login_required
def post_job(request):

    if request.user.role != "client":

        return render(
            request,
            "jobs/job_list.html",
            {
                "jobs": Job.objects.all().order_by("-created_at"),
                "error": "Only clients can post jobs.",
            }
        )

    if request.method == "POST":

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.client = request.user

            job.save()

            return redirect("job_list")

    else:

        form = JobForm()

    return render(
        request,
        "jobs/post_job.html",
        {
            "form": form,
        }
    )


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
    if request.user.role != "student":

        return render(
            request,
            "jobs/job_list.html",
            {
                "jobs": Job.objects.all().order_by("-created_at"),
                "error": "Only students can apply for jobs.",
            }
        )

    # Prevent applying to own job
    if job.client == request.user:

        return render(
            request,
            "jobs/job_list.html",
            {
                "jobs": Job.objects.all().order_by("-created_at"),
                "error": "You cannot apply to your own job.",
            }
        )

    # Prevent duplicate applications
    existing_application = Application.objects.filter(
        job=job,
        student=request.user
    ).first()

    if existing_application:

        return render(
            request,
            "jobs/job_list.html",
            {
                "jobs": Job.objects.all().order_by("-created_at"),
                "error": "You have already applied for this job.",
            }
        )

    # Show application form
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
                status="Pending",
            )

            return redirect("student_dashboard")

    return render(
        request,
        "applications/apply.html",
        {
            "job": job,
        }
    )


# ============================================================
# VIEW APPLICANTS
# ============================================================

@login_required
def view_applicants(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        client=request.user
    )

    return render(
        request,
        "jobs/view_applicants.html",
        _applicants_context(job),
    )


@login_required
def scan_applicant_resume(request, application_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if request.user.role != "client":
        return redirect("client_dashboard")

    application = get_object_or_404(
        Application.objects.select_related("job", "student"),
        id=application_id,
        job__client=request.user,
    )
    profile, _ = StudentProfile.objects.get_or_create(user=application.student)
    resume = profile.resume
    context = _applicants_context(application.job)
    context["scanned_application_id"] = application.id

    if not resume:
        context["scan_error"] = "This student has not uploaded a resume."
    elif not resume.name.lower().endswith(".pdf"):
        context["scan_error"] = "Only PDF resumes can be scanned."
    else:
        try:
            if resume.size > MAX_RESUME_FILE_SIZE:
                raise ValueError("Resume PDFs must be 10 MB or smaller.")
            resume.open("rb")
            try:
                header = resume.read(1024)
                if b"%PDF-" not in header:
                    raise ValueError("The uploaded file is not a valid PDF.")
                resume.seek(0)
                resume_text = extract_resume_text(resume)
            finally:
                resume.close()
            context["scan_result"] = analyze_resume(
                resume_text,
                application.job,
                profile,
            )
        except ValueError as error:
            context["scan_error"] = str(error)
        except (OSError, PdfReadError, PdfStreamError):
            context["scan_error"] = (
                "The PDF could not be read. Please check the file and try again."
            )

    return render(request, "jobs/view_applicants.html", context)
# ============================================================
# ACCEPT APPLICATION
# ============================================================

@login_required
def accept_application(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id
    )

    # Only the owner/client of the job can accept
    if application.job.client != request.user:
        return redirect("client_dashboard")

    # Update application status
    application.status = "Accepted"
    application.save()

    # Send automatic message to the student
    Message.objects.create(
        sender=request.user,
        receiver=application.student,
        message=(
            f"Your application for '{application.job.title}' "
            "has been accepted. Congratulations!"
        )
    )

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

    # Only the owner/client of the job can reject
    if application.job.client != request.user:

        return redirect("client_dashboard")

    application.status = "Rejected"

    application.save()

    return redirect(
        "view_applicants",
        job_id=application.job.id
    )