from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'preview', 'owner', 'price', 'time_update', 'time_last_send']
    readonly_fields = ['time_update', 'time_last_send']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = ['title', 'description', 'preview', 'link_video', 'course', 'owner', 'time_update']
    readonly_fields = ['time_update']
