from django.db import models

from lms.constants import TITLE_LEN
from users.models import User


class Course(models.Model):
    title = models.CharField(
        "Название",
        max_length=TITLE_LEN,
    )
    description = models.TextField(
        "Описание",
    )
    preview = models.ImageField(
        "Превью",
        upload_to="courses/previews/",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self) -> str:
        return str(self.title)


class Lesson(models.Model):
    title = models.CharField(
        "Название",
        max_length=TITLE_LEN,
    )
    description = models.TextField(
        "Описание",
    )
    preview = models.ImageField(
        "Превью",
        upload_to="lessons/previews/",
    )
    video_url = models.URLField(
        "Ссылка на видео",
    )
    course = models.ForeignKey(
        Course,
        related_name="lessons",
        on_delete=models.CASCADE,
        verbose_name="Курс",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:
        return str(self.title)
