import news.views

from django.urls import path


app_name = "news"
urlpatterns = [
    path("", news.views.news_list_view, name="list"),
    path("<int:news_id>/", news.views.news_detail_view, name="detail"),
]
