from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('textbooks/', views.textbooks_view, name='textbooks'),
    path('faq/', views.faq_view, name='faq'),
    path('chat-ask/', views.chat_ask, name='chat_ask'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('confirm-email/<uidb64>/<token>/', views.confirm_email_view, name='confirm_email'),
]