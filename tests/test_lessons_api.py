from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from lms.models import Course, Lesson
from users.models import User


class LessonTests(APITestCase):
    user: User
    moderator: User
    course: Course
    lesson: Lesson
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
            preview="media/images/preview.jpg",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Тестовое описание урока",
            preview="media/images/preview.jpg",
            video_url="https://youtube.com/firstvideo",
            course=self.course,
            owner=self.user,
        )
        self.user_token = str(
            RefreshToken.for_user(self.user).access_token,
        )
        self.moderator_token = str(
            RefreshToken.for_user(self.moderator).access_token,
        )

    def test_create_lesson(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )
        data: dict[str, str | int] = {
            "title": "Новый урок",
            "description": "Описание нового тестового урока",
            "video_url": "https://youtube.com/newvideo",
            "course": self.course.id,
        }

        response: Response = self.client.post(
            "/api/lessons/create/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_update_lesson(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.moderator_token}",
        )
        data: dict[str, str | int] = {
            "title": "Обновлен тестовый урок",
            "description": "Обновленное описание тестового урока",
            "video_url": "https://youtube.com/updatedvideo",
            "course": self.lesson.course.id,
        }

        response: Response = self.client.put(
            f"/api/lessons/{self.lesson.id}/edit/",
            data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, data["title"])

    def test_delete_lesson(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        response: Response = self.client.delete(
            f"/api/lessons/{self.lesson.id}/delete/",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_get_lesson(self) -> None:
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.user_token}",
        )

        response: Response = self.client.get(
            f"/api/lessons/{self.lesson.id}/",
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.lesson.title)
