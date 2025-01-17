from celery import shared_task
from django.core.mail import send_mail

from lms.models import CourseSubscription


@shared_task
def send_course_update_notification(course_id, lesson_title):
    subscriptions = CourseSubscription.objects.filter(course_id=course_id)
    recipient_emails = subscriptions.values_list("user__email", flat=True)

    send_mail(
        subject=f"Обновление курса: {lesson_title}",
        message=(
            "Уважаемый студент! В курсе "
            f"'{subscriptions[0].course.title}' "
            f"появился новый урок: {lesson_title}."
        ),
        from_email="noreply@pudemy.com",
        recipient_list=list(recipient_emails),
        fail_silently=False,
    )
