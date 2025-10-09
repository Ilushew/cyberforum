from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'core'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('textbooks/', views.textbooks_view, name='textbooks'),
    path('moderator/textbooks/', views.textbook_moderator_list, name='textbook_moderator_list'),
    path('moderator/textbooks/create/', views.textbook_create, name='textbook_create'),
    path('moderator/textbooks/delete/<int:textbook_id>/', views.textbook_delete, name='textbook_delete'),
    path('faq/', views.faq_view, name='faq'),
    path('events/', views.events_view, name='events'),
    path('events/<int:event_id>/', views.event_detail_view, name='event_detail'),
    path('documentation/', views.documentation_view, name='documentation'),
    path('chat-ask/', views.chat_ask, name='chat_ask'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email_view, name='confirm_email'),
    path('api/events/', views.events_api_view, name='events_api'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    path('moderator/news/', views.news_moderator_list, name='news_moderator_list'),
    path('moderator/news/create/', views.news_create, name='news_create'),
    path('moderator/news/<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('moderator/news/<int:news_id>/delete/', views.news_delete, name='news_delete'),
    path('moderator/events/', views.event_moderator_list, name='event_moderator_list'),
    path('moderator/events/create/', views.event_create, name='event_create'),
    path('moderator/events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('moderator/events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('moderator/documentation/', views.documentation_moderator_list, name='documentation_moderator_list'),
    path('moderator/documentation/create/', views.documentation_create, name='documentation_create'),
    path('moderator/documentation/<int:doc_id>/delete/', views.documentation_delete, name='documentation_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


