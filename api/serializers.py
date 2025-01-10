from rest_framework import serializers

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

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "lessons",
            "lesson_count",
            "is_subscribed",
        )

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        return CourseSubscription.objects.filter(
            user=self.context.get("request").user,
            course=obj,
        ).exists()
