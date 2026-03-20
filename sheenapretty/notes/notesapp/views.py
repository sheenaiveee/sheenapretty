from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from .forms import CourseForm, NoteForm, SignUpForm
from .models import Course, Note


def _user_course_queryset(request):
	return Course.objects.filter(owner=request.user)


def _user_note_queryset(request):
	return Note.objects.filter(owner=request.user).select_related('course')


@login_required
def dashboard(request):
	recent_notes = _user_note_queryset(request).order_by('-updated_at')[:10]
	pinned_notes = _user_note_queryset(request).filter(pinned=True).order_by('-updated_at')[:10]
	courses = _user_course_queryset(request).order_by('name')
	return render(
		request,
		'notesapp/dashboard.html',
		{
			'recent_notes': recent_notes,
			'pinned_notes': pinned_notes,
			'courses': courses,
		},
	)


@login_required
def course_list(request):
	courses = _user_course_queryset(request).order_by('name')
	return render(request, 'notesapp/course_list.html', {'courses': courses})


@login_required
@require_http_methods(['GET', 'POST'])
def course_create(request):
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			course = form.save(commit=False)
			course.owner = request.user
			course.save()
			return redirect('course_detail', course_id=course.id)
	else:
		form = CourseForm()

	return render(request, 'notesapp/course_form.html', {'form': form})


@login_required
def course_detail(request, course_id: int):
	course = get_object_or_404(_user_course_queryset(request), id=course_id)
	notes = course.notes.filter(owner=request.user).order_by('-pinned', '-updated_at')
	return render(request, 'notesapp/course_detail.html', {'course': course, 'notes': notes})


@login_required
@require_http_methods(['GET', 'POST'])
def note_create(request):
	if request.method == 'POST':
		form = NoteForm(request.POST)
		form.fields['course'].queryset = _user_course_queryset(request)
		if form.is_valid():
			note = form.save(commit=False)
			note.owner = request.user
			note.save()
			return redirect('note_detail', note_id=note.id)
	else:
		initial = {}
		course_id = request.GET.get('course')
		if course_id:
			try:
				course_id_int = int(course_id)
			except ValueError:
				raise Http404
			if _user_course_queryset(request).filter(id=course_id_int).exists():
				initial['course'] = course_id_int

		form = NoteForm(initial=initial)
		form.fields['course'].queryset = _user_course_queryset(request)

	return render(request, 'notesapp/note_form.html', {'form': form, 'mode': 'create'})


@login_required
def note_detail(request, note_id: int):
	note = get_object_or_404(_user_note_queryset(request), id=note_id)
	return render(request, 'notesapp/note_detail.html', {'note': note})


@login_required
@require_http_methods(['GET', 'POST'])
def note_edit(request, note_id: int):
	note = get_object_or_404(_user_note_queryset(request), id=note_id)
	if request.method == 'POST':
		form = NoteForm(request.POST, instance=note)
		form.fields['course'].queryset = _user_course_queryset(request)
		if form.is_valid():
			form.save()
			return redirect('note_detail', note_id=note.id)
	else:
		form = NoteForm(instance=note)
		form.fields['course'].queryset = _user_course_queryset(request)

	return render(request, 'notesapp/note_form.html', {'form': form, 'mode': 'edit', 'note': note})


@login_required
@require_http_methods(['GET', 'POST'])
def note_delete(request, note_id: int):
	note = get_object_or_404(_user_note_queryset(request), id=note_id)
	if request.method == 'POST':
		note.delete()
		return redirect('dashboard')

	return render(request, 'notesapp/note_confirm_delete.html', {'note': note})


@login_required
@require_POST
def note_toggle_pin(request, note_id: int):
	note = get_object_or_404(_user_note_queryset(request), id=note_id)
	note.pinned = not note.pinned
	note.save(update_fields=['pinned', 'updated_at'])
	next_url = request.POST.get('next')
	if next_url:
		return redirect(next_url)
	return redirect('note_detail', note_id=note.id)


@require_http_methods(['GET', 'POST'])
def signup(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('dashboard')
	else:
		form = SignUpForm()

	return render(request, 'registration/signup.html', {'form': form})
