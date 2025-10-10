from django.urls import path
from . import views

app_name = 'moderation'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Новости
    path('news/', views.news_moderator_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('news/<int:news_id>/delete/', views.news_delete, name='news_delete'),

    # События
    path('events/', views.event_moderator_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),

    # Документы
    path('documentation/', views.documentation_moderator_list, name='documentation_list'),
    path('documentation/create/', views.documentation_create, name='documentation_create'),
    path('documentation/<int:doc_id>/delete/', views.documentation_delete, name='documentation_delete'),

    path('courses/', views.course_moderator_list, name='course_moderator_list'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', views.course_delete, name='course_delete'),

    path('courses/<int:course_id>/lessons/', views.lesson_list, name='lesson_list'),
    path('courses/<int:course_id>/lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', views.lesson_delete, name='lesson_delete'),

]