from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsModerator, IsOwner
from api.serializers import CourseSerializer
from lms.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ("list", "retrieve", "update", "partial_update"):
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action in ("create", "destroy"):
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
