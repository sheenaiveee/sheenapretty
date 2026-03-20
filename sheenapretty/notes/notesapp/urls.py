from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('notes/new/', views.note_create, name='note_create'),
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('notes/<int:note_id>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:note_id>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:note_id>/pin/', views.note_toggle_pin, name='note_toggle_pin'),
]
