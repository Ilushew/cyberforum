from django.urls import path
from . import views

app_name = 'moderation'
urlpatterns = [
    path('', views.moderator_dashboard, name='dashboard'),

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
]