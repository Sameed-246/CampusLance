from .models import Message


def unread_messages(request):
    """
    Makes unread message information available
    to every template.
    """

    if not request.user.is_authenticated:
        return {
            "unread_message_count": 0
        }

    count = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).count()

    return {
        "unread_message_count": count
    }