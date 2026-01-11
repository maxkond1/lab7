from rest_framework import generics, permissions
from .models import Poll, Vote
from .serializers import PollSerializer, VoteSerializer

class PollListAPI(generics.ListAPIView):
    queryset = Poll.objects.filter(is_active=True)
    serializer_class = PollSerializer
    permission_classes = [permissions.AllowAny]

class PollDetailAPI(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [permissions.AllowAny]

class VoteCreateAPI(generics.CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
