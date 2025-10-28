from django.urls import path

from . import views, admin_views


app_name = "courses"

urlpatterns = [
    path("", views.course_list_view, name="list"),
    path("<int:course_id>/", views.course_detail_view, name="detail"),
    path("lesson/<int:lesson_id>/", views.lesson_view, name="lesson"),
    path("lesson/<int:lesson_id>/test/", views.submit_test_view, name="test"),
    path("admin/analytics/", admin_views.test_analytics_view, name="test_analytics"),
    path(
        "certificate/<int:course_id>/",
        views.download_certificate,
        name="download_certificate",
    ),
]
