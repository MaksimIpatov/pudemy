import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import LessonPagination
from api.permissions import IsModerator, IsOwner, IsOwnerOrModerator
from api.serializers import LessonSerializer, PaymentSerializer
from api.utils import StripeService
from lms.models import Course, CourseSubscription, Lesson
from payments.models import Payment


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrModerator)
    pagination_class = LessonPagination


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrModerator)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner)


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "method")
    permission_classes = (IsAuthenticated,)
    ordering_fields = ("date",)
    ordering = ("-date",)


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")
        payment = serializer.save(user=self.request.user)
        stripe_service = StripeService()
        try:
            price = stripe_service.create_price(
                amount=payment.amount,
                product_name=course.title,
            )
            session = stripe_service.create_session(
                price_id=price["id"],
                success_url="http://127.0.0.1:8000/api/cources/",
                cancel_url="http://127.0.0.1:8000/api/cources/",
            )
            payment.stripe_session_id = session["id"]
            payment.save()
        except Exception as err:
            payment.delete()
            raise serializers.ValidationError({"detail": str(err)})


class PaymentRetrieveAPIView(RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)


class PaymentUpdateAPIView(UpdateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsModerator, IsAuthenticated)


class PaymentDestroyAPIView(DestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)


class PaymentStatusAPIView(APIView):
    """Проверка статуса платежной сессии."""

    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        try:
            session = StripeService.retrieve_session(session_id)
            return Response(
                {
                    "id": session.get("id"),
                    "payment_status": session.get("payment_status"),
                    "amount_total": session.get("amount_total"),
                    "currency": session.get("currency"),
                    "customer_email": session.get("customer_email"),
                },
                status=status.HTTP_200_OK,
            )
        except stripe.error.InvalidRequestError as err:
            return Response(
                {"detail": err},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as err:
            return Response(
                {"detail": "Произошла ошибка при получении статуса платежа."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        course = Course.objects.get(id=request.data.get("course_id"))

        subscription, created = CourseSubscription.objects.get_or_create(
            user=request.user,
            course=course,
        )
        if not created:
            subscription.delete()
            return Response(
                data={"message": f"Вы отписались от курса '{course.title}'"},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"message": f"Вы подписались на курс '{course.title}'"},
            status=status.HTTP_201_CREATED,
        )
