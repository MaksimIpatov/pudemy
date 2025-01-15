from rest_framework import serializers

from api.utils import StripeService
from api.validators import VideoUrlValidator
from lms.models import Course, CourseSubscription, Lesson
from payments.models import Payment
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "date",
            "course",
            "lesson",
            "amount",
            "method",
            "stripe_session_id",
        )
        read_only_fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(
        many=True,
        read_only=True,
        source="payment_set",
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "phone_number",
            "city",
            "avatar",
            "payments",
            "is_staff",
            "is_active",
        )
        read_only_fields = ("id",)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "video_url",
            "course",
            "owner",
        )
        read_only_fields = ("id", "owner")
        validators = [
            VideoUrlValidator(field="video_url"),
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    stripe_url = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "lessons",
            "lesson_count",
            "price",
            "is_subscribed",
            "stripe_url",
        )

    def get_lesson_count(self, obj) -> int:
        return obj.lessons.count()

    def get_is_subscribed(self, obj) -> bool:
        return CourseSubscription.objects.filter(
            user=self.context.get("request").user,
            course=obj,
        ).exists()

    def get_stripe_url(self, obj) -> dict | str:
        """
        Создание Stripe-продукта, цены и сессии для оплаты курса.
        Возвращает URL сессии Stripe.
        """
        try:
            product = StripeService.create_product(
                name=obj.title,
                description=obj.description,
            )
            price = StripeService.create_price(
                amount=obj.price,
                product_name=product["name"],
            )
            session = StripeService.create_session(
                price_id=price["id"],
                success_url="http://127.0.0.1:8000/api/courses/",
                cancel_url="http://127.0.0.1:8000/api/courses/",
            )
            return session["url"]
        except Exception as err:
            return str(err)
