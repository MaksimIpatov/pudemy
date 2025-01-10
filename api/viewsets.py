from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.pagination import CoursePagination
from api.permissions import IsModerator, IsOwner
from api.serializers import CourseSerializer
from lms.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("title")
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
