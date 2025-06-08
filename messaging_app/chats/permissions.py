from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to authenticated users who are participants of the conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', None)

        if conversation and request.user in conversation.participants.all():
            if request.method in permissions.SAFE_METHODS or request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
                return True

        return False
