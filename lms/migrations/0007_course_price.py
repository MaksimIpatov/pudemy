# Generated by Django 4.2.17 on 2025-01-14 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0006_alter_lesson_preview"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.IntegerField(
                default=100000, verbose_name="Стоимость курса"
            ),
        ),
    ]
