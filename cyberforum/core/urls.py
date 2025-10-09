from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('textbooks/', views.textbooks_view, name='textbooks'),  # ← добавлено
    path('events/', views.events_view, name='events'),
    path('chat-ask/', views.chat_ask, name='chat_ask'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email_view, name='confirm_email'),
    path('news/', views.news_list_view, name='news_list'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('moderator/news/', views.news_moderator_list, name='news_moderator_list'),
    path('moderator/news/create/', views.news_create, name='news_create'),
    path('moderator/news/<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('moderator/news/<int:news_id>/delete/', views.news_delete, name='news_delete'),
]