from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    PaymentCreateAPIView,
    PaymentDestroyAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    PaymentUpdateAPIView,
)
from api.viewsets import CourseViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"profile", UserProfileViewSet, basename="profile")

urlpatterns = [
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
]
