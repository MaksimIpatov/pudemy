from django.db import models

from lms.constants import TITLE_LEN


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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self) -> str:
        return str(self.title)
