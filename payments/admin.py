from django.contrib import admin

from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "amount")
    search_fields = (
        "user__email",
        "course__title",
        "lesson__title",
    )
    list_filter = ("method",)
    ordering = ("-date",)
    autocomplete_fields = ("user", "course", "lesson")
