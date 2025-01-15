from django.db import models

from lms.constants import NULL_BLANK_TRUE, TITLE_LEN
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
        **NULL_BLANK_TRUE,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )
    price = models.IntegerField(
        "Стоимость курса",
        default=100_000,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ("title",)

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
        **NULL_BLANK_TRUE,
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
        ordering = ("title",)

    def __str__(self) -> str:
        return str(self.title)


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Подписчик",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"
        ordering = ("course", "user")
        unique_together = ("user", "course")

    def __str__(self) -> str:
        return f"{self.user.email} подписан на курс {self.course.title}"
