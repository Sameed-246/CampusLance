from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Message


User = get_user_model()


# ============================================================
# SEND MESSAGE
# ============================================================

@login_required
def send_message(request, user_id):

    receiver = get_object_or_404(
        User,
        id=user_id
    )

    # Don't allow messaging yourself
    if receiver == request.user:
        return redirect("message_inbox")

    if request.method == "POST":

        message_text = request.POST.get(
            "message",
            ""
        ).strip()

        if message_text:

            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                message=message_text
            )

            return redirect(
                "conversation",
                user_id=receiver.id
            )

    return render(
        request,
        "messaging/send_message.html",
        {
            "receiver": receiver
        }
    )


# ============================================================
# CONVERSATION
# ============================================================

@login_required
def conversation(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    # Get messages in BOTH directions
    messages = Message.objects.filter(
        Q(
            sender=request.user,
            receiver=other_user
        )
        |
        Q(
            sender=other_user,
            receiver=request.user
        )
    ).select_related(
        "sender",
        "receiver"
    ).order_by(
        "created_at"
    )

    # Mark all messages from the other user as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(
        is_read=True
    )

    return render(
        request,
        "messaging/conversation.html",
        {
            "other_user": other_user,
            "messages": messages
        }
    )


# ============================================================
# MESSAGE INBOX
# ============================================================

@login_required
def message_inbox(request):

    # Get every message involving the logged-in user
    all_messages = Message.objects.filter(
        Q(sender=request.user)
        |
        Q(receiver=request.user)
    ).select_related(
        "sender",
        "receiver"
    ).order_by(
        "-created_at"
    )

    conversations = {}

    for message in all_messages:

        # Determine the other person
        if message.sender == request.user:
            other_user = message.receiver
        else:
            other_user = message.sender

        # Only create one inbox entry per person
        if other_user.id not in conversations:

            # Check whether there are ANY unread messages
            # from this person to the current user.
            unread_exists = Message.objects.filter(
                sender=other_user,
                receiver=request.user,
                is_read=False
            ).exists()

            conversations[other_user.id] = {
                "user": other_user,
                "message": message,
                "unread": unread_exists,
            }

    return render(
        request,
        "messaging/inbox.html",
        {
            "conversations": conversations.values()
        }
    )