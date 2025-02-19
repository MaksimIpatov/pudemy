from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.apps import ApiConfig
from api.views import (
    CourseSubscriptionAPIView,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    PaymentCreateAPIView,
    PaymentDestroyAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentStatusAPIView,
    PaymentUpdateAPIView,
)
from api.viewsets import CourseViewSet

app_name = ApiConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path(
        "courses/subscribe/",
        CourseSubscriptionAPIView.as_view(),
        name="course-subscribe",
    ),
    path("", include(router.urls)),
    path(
        "lessons/",
        LessonListAPIView.as_view(),
        name="lesson-list",
    ),
    path(
        "lessons/create/",
        LessonCreateAPIView.as_view(),
        name="lesson-create",
    ),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson-detail",
    ),
    path(
        "lessons/<int:pk>/edit/",
        LessonUpdateAPIView.as_view(),
        name="lesson-update",
    ),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyAPIView.as_view(),
        name="lesson-delete",
    ),
    path(
        "payments/",
        PaymentListAPIView.as_view(),
        name="payment-list",
    ),
    path(
        "payments/create/",
        PaymentCreateAPIView.as_view(),
        name="payment-create",
    ),
    path(
        "payments/<int:pk>/",
        PaymentRetrieveAPIView.as_view(),
        name="payment-retrieve",
    ),
    path(
        "payments/<int:pk>/edit/",
        PaymentUpdateAPIView.as_view(),
        name="payment-update",
    ),
    path(
        "payments/<int:pk>/delete/",
        PaymentDestroyAPIView.as_view(),
        name="payment-delete",
    ),
    path(
        "payments/status/<str:session_id>/",
        PaymentStatusAPIView.as_view(),
        name="payment-status",
    ),
]
