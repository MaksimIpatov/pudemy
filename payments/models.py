from django.conf import settings
from django.db import models

from lms.models import Course, Lesson
from payments.constants import (
    NULL_BLANK_TRUE,
    PAYMENT_AMOUNT_MAX_DIGIT,
    PAYMENT_METHODS,
)


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    date = models.DateTimeField(
        "Дата оплаты",
        auto_now_add=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        **NULL_BLANK_TRUE,
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        **NULL_BLANK_TRUE,
        verbose_name="Оплаченный урок",
    )
    amount = models.DecimalField(
        "Сумма оплаты",
        max_digits=PAYMENT_AMOUNT_MAX_DIGIT,
        decimal_places=2,
    )
    method = models.CharField(
        "Способ оплаты",
        max_length=10,
        choices=tuple(PAYMENT_METHODS.items()),
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self) -> str:
        return f"{self.course} - {self.lesson} | [{self.method}]"
