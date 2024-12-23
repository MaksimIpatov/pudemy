from django.contrib import admin

from lms.models import Course, Lesson


class LessonInline(admin.TabularInline):
    """
    Инлайн-форма для отображения уроков, связанных с курсом.
    """

    model = Lesson
    extra = 1
    fields = (
        "title",
        "description",
        "video_url",
        "preview",
    )


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "preview",
        "lesson_count",
    )
    search_fields = ("title", "description")
    list_filter = ("title",)
    prepopulated_fields = {"title": ("description",)}
    inlines = [LessonInline]

    def lesson_count(self, obj) -> int:
        """
        Отображает количество уроков в курсе.
        """
        return obj.lessons.count()

    lesson_count.short_description = "Количество уроков"


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "video_url",
        "preview",
    )
    search_fields = ("title", "description", "video_url")
    list_filter = ("course",)
    list_select_related = ("course",)
