from rest_framework import serializers

from lms.models import Course, Lesson
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
        )
        read_only_fields = ("id",)


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "preview",
            "lessons",
            "lesson_count",
        )

    def get_lesson_count(self, obj):
        return obj.lessons.count()
