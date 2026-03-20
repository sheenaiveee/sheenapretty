from django.contrib import admin

from .models import Course, Note


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
	list_display = ('name', 'owner', 'updated_at')
	search_fields = ('name', 'owner__username', 'owner__email')
	list_filter = ('updated_at',)


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'course', 'note_date', 'pinned', 'updated_at')
	search_fields = ('title', 'content', 'owner__username', 'owner__email', 'course__name')
	list_filter = ('pinned', 'updated_at', 'course')
