import documentation.views

from django.urls import path


app_name = "documentation"
urlpatterns = [
    path("", documentation.views.documentation_view, name="list"),
]
