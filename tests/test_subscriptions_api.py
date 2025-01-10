from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import Course
from users.models import User


class CourseSubscriptionTests(APITestCase):
    user: User
    course: Course
    user_token: str

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="first_user@mail.ru",
            password="test#1234",
        )
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Тестовое описание курса",
            preview="media/images/preview.jpg",
            owner=self.user,
        )
        self.user_token = str(
            RefreshToken.for_user(self.user).access_token,
        )

    def test_subscribe_to_course(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        data: dict[str, int] = {"course_id": self.course.id}

        response: Response = self.client.post(
            "/api/courses/subscribe/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            response.data["message"],
            f"Вы подписались на курс '{self.course.title}'",
        )

    def test_unsubscribe_from_course(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        data: dict[str, int] = {"course_id": self.course.id}

        response: Response = self.client.post(
            "/api/courses/subscribe/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        response: Response = self.client.post(
            "/api/courses/subscribe/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["message"],
            f"Вы отписались от курса '{self.course.title}'",
        )

    def test_get_subscription_status(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        response: Response = self.client.get(
            f"/api/courses/{self.course.id}/",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertFalse(response.data["is_subscribed"])
