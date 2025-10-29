import search.views

from django.urls import path


app_name = "search"

urlpatterns = [
    path("", search.views.search_view, name="results"),
]
