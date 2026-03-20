from django.conf import settings
from django.db import models
from django.utils import timezone


class Course(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='courses',
	)
	name = models.CharField(max_length=120)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['name']
		constraints = [
			models.UniqueConstraint(
				fields=['owner', 'name'],
				name='unique_course_name_per_owner',
			),
		]

	def __str__(self) -> str:
		return self.name


class Note(models.Model):
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name='notes',
	)
	course = models.ForeignKey(
		Course,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='notes',
	)

	title = models.CharField(max_length=200)
	note_date = models.DateField(default=timezone.localdate)
	content = models.TextField(blank=True)
	pinned = models.BooleanField(default=False)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-pinned', '-updated_at']

	def __str__(self) -> str:
		return self.title

# Create your models here.
