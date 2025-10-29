import courses.admin_views
import courses.views

from django.urls import path


app_name = "courses"

urlpatterns = [
    path("", courses.views.course_list_view, name="list"),
    path("<int:course_id>/", courses.views.course_detail_view, name="detail"),
    path("lesson/<int:lesson_id>/", courses.views.lesson_view, name="lesson"),
    path("lesson/<int:lesson_id>/test/", courses.views.submit_test_view, name="test"),
    path("admin/analytics/", courses.admin_views.test_analytics_view, name="test_analytics"),
    path(
        "certificate/<int:course_id>/",
        courses.views.download_certificate,
        name="download_certificate",
    ),
]
