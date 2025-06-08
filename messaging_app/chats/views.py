from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__email']

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    def get_queryset(self):
        # Return only conversations the user is a participant in
        return Conversation.objects.filter(participants=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                if self.request.user not in conversation.participants.all():
                    raise PermissionDenied("You are not a participant of this conversation.")
                return Message.objects.filter(conversation=conversation)
            except Conversation.DoesNotExist:
                raise PermissionDenied("Conversation not found.")
        # Default: filter only messages where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = Conversation.objects.get(id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages in this conversation.")
        serializer.save(sender=self.request.user, conversation=conversation)
