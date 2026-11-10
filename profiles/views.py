from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import StudentProfile
from .forms import StudentProfileForm
from accounts.models import CustomUser


@login_required
def profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    return render(request, "profiles/profile.html", {
        "profile": profile
    })


@login_required
def edit_profile(request):
    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = StudentProfileForm(instance=profile)

    return render(request, "profiles/edit_profile.html", {
        "form": form
    })


@login_required
def student_profile(request, student_id):
    student = get_object_or_404(
        CustomUser,
        id=student_id,
        role="student"
    )

    profile, created = StudentProfile.objects.get_or_create(
        user=student
    )

    return render(request, "profiles/student_profile.html", {
        "student": student,
        "profile": profile
    })