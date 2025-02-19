# Generated by Django 4.2.17 on 2025-01-14 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="stripe_session_id",
            field=models.CharField(
                blank=True,
                help_text="Идентификатор платежной сессии в Stripe",
                max_length=255,
                null=True,
                verbose_name="ID сессии Stripe",
            ),
        ),
    ]
