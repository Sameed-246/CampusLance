from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CustomUserRegistrationForm


# ============================================================
# HOME PAGE
# ============================================================

def home(request):

    return render(
        request,
        "accounts/home.html"
    )


# ============================================================
# USER REGISTRATION
# ============================================================

def register(request):

    if request.method == "POST":

        form = CustomUserRegistrationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Registration Successful! Please login."
            )

            return redirect("login")

    else:

        form = CustomUserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


# ============================================================
# LOGIN SELECTION PAGE
# ============================================================

def user_login(request):

    return render(
        request,
        "accounts/login.html"
    )


# ============================================================
# STUDENT LOGIN
# ============================================================

def student_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ------------------------------------------------
            # MAKE SURE USER IS A STUDENT
            # ------------------------------------------------

            if user.role != "student":

                messages.error(
                    request,
                    "This account is registered as a Client. "
                    "Please use the Client Login page."
                )

                return redirect("client_login")

            # ------------------------------------------------
            # LOGIN STUDENT
            # ------------------------------------------------

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome back! Student login successful."
            )

            return redirect(
                "student_dashboard"
            )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "accounts/student_login.html"
    )


# ============================================================
# CLIENT LOGIN
# ============================================================

def client_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # ------------------------------------------------
            # MAKE SURE USER IS A CLIENT
            # ------------------------------------------------

            if user.role != "client":

                messages.error(
                    request,
                    "This account is registered as a Student. "
                    "Please use the Student Login page."
                )

                return redirect("student_login")

            # ------------------------------------------------
            # LOGIN CLIENT
            # ------------------------------------------------

            login(
                request,
                user
            )

            messages.success(
                request,
                "Welcome back! Client login successful."
            )

            return redirect(
                "client_dashboard"
            )

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "accounts/client_login.html"
    )


# ============================================================
# USER LOGOUT
# ============================================================

def user_logout(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully!"
    )

    return redirect(
        "home"
    )