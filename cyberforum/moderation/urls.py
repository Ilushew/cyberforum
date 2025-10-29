import moderation.views

from django.urls import path


app_name = "moderation"
urlpatterns = [
    path("", moderation.views.dashboard, name="dashboard"),
    # Новости
    path("news/", moderation.views.news_moderator_list, name="news_list"),
    path("news/create/", moderation.views.news_create, name="news_create"),
    path("news/<int:news_id>/edit/", moderation.views.news_edit, name="news_edit"),
    path("news/<int:news_id>/delete/", moderation.views.news_delete, name="news_delete"),
    # События
    path("events/", moderation.views.event_moderator_list, name="event_list"),
    path("events/create/", moderation.views.event_create, name="event_create"),
    path("events/<int:event_id>/edit/", moderation.views.event_edit, name="event_edit"),
    path("events/<int:event_id>/delete/", moderation.views.event_delete, name="event_delete"),
    # Документы

    path(
        "documentation/", moderation.views.documentation_moderator_list, name="documentation_list"
    ),
    path(
        "documentation/create/", moderation.views.documentation_create, name="documentation_create"
    ),
    path(
        "documentation/<int:doc_id>/delete/",
        moderation.views.documentation_delete,
        name="documentation_delete",
    ),

    path('courses/', moderation.views.course_moderator_list, name='course_moderator_list'),
    path('courses/create/', moderation.views.course_create, name='course_create'),
    path('courses/<int:course_id>/edit/', moderation.views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/delete/', moderation.views.course_delete, name='course_delete'),

    path('courses/<int:course_id>/lessons/', moderation.views.lesson_list, name='lesson_list'),
    path('courses/<int:course_id>/lessons/create/', moderation.views.lesson_create, name='lesson_create'),
    path('lessons/<int:lesson_id>/edit/', moderation.views.lesson_edit, name='lesson_edit'),
    path('lessons/<int:lesson_id>/delete/', moderation.views.lesson_delete, name='lesson_delete'),

]
