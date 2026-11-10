from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "student/",
        views.student_dashboard,
        name="student_dashboard"
    ),

    path(
        "client/",
        views.client_dashboard,
        name="client_dashboard"
    ),

    path(
        "ai-assistant/",
        views.ai_assistant,
        name="ai_assistant"
    ),
]