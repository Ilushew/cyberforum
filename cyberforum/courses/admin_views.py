from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import TestResult, Course


@staff_member_required
def test_analytics_view(request):
    course_stats = (
        TestResult.objects.select_related("lesson__course")
        .values("lesson__course__title")
        .annotate(avg_percent=Avg("percent"))
        .order_by("-avg_percent")
    )

    daily_stats = (
        TestResult.objects.extra(select={"date": "date(completed_at)"})
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )

    context = {
        "course_labels": [item["lesson__course__title"] for item in course_stats],
        "course_data": [float(item["avg_percent"]) for item in course_stats],
        "daily_labels": [str(item["date"]) for item in daily_stats],
        "daily_data": [item["count"] for item in daily_stats],
    }
    return render(request, "admin/test_analytics.html", context)
