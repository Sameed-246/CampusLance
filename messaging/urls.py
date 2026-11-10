from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.message_inbox,
        name="message_inbox"
    ),

    path(
        "conversation/<int:user_id>/",
        views.conversation,
        name="conversation"
    ),

    path(
        "send/<int:user_id>/",
        views.send_message,
        name="send_message"
    ),

]