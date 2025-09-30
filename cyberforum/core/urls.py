from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('events/', views.events_view, name='events'),
    path('chat-ask/', views.chat_ask, name='chat_ask'),
]