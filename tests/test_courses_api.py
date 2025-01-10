from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import Course
from users.models import User


class CourseTests(APITestCase):
    user: User
    moderator: User
    course: Course
    user_token: str
    moderator_token: str

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email="first_user@mail.ru",
            password="test#1234",
        )
        self.moderator = User.objects.create_user(
            email="moder_user@mail.ru",
            password="test#1234",
            is_staff=True,
        )
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Тестовое описание курса",
            owner=self.user,
        )
        self.user_token = str(
            RefreshToken.for_user(self.user).access_token,
        )
        self.moderator_token = str(
            RefreshToken.for_user(self.moderator).access_token,
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

    def test_create_course(self) -> None:
        url: str = reverse("api:course-list")
        data: dict[str, str] = {
            "title": "Новый тестовый курс",
            "description": "Описание нового тестового курса",
        }

        response: Response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(Course.objects.count(), 2)

    def test_delete_course_as_owner(self) -> None:
        url: str = reverse(
            "api:course-detail",
            kwargs={"pk": self.course.id},
        )

        response: Response = self.client.delete(url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Course.objects.count(), 0)

    def test_delete_course_as_moderator(self) -> None:
        url: str = reverse(
            "api:course-detail",
            kwargs={"pk": self.course.id},
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )

        response: Response = self.client.delete(url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Course.objects.count(), 0)

    def test_delete_course_unauthorized(self) -> None:
        second_user: User = User.objects.create_user(
            email="second_user@mail.ru",
            password="password",
        )
        second_user_token: str = str(
            RefreshToken.for_user(second_user).access_token,
        )
        url: str = reverse(
            "api:course-detail",
            kwargs={"pk": self.course.id},
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {second_user_token}",
        )

        response: Response = self.client.delete(url, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_list_courses(self) -> None:
        url: str = reverse("api:course-list")

        response: Response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_update_course(self) -> None:
        url: str = reverse(
            "api:course-detail",
            kwargs={"pk": self.course.id},
        )
        data: dict[str, str] = {
            "title": "Обновлен тестовый курс",
            "description": "Обновленное описание тестового курса",
        }

        response: Response = self.client.put(
            url,
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, data["title"])
        self.assertEqual(self.course.description, data["description"])
