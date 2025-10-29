import news.models

from django.shortcuts import render, get_object_or_404


def news_list_view(request):
    news_list = news.models.News.objects.filter(is_published=True).order_by("-created_at")
    return render(request, "news/list.html", {"news_list": news_list})


def news_detail_view(request, news_id):
    news_item = get_object_or_404(news.models.News, id=news_id, is_published=True)
    return render(request, "news/detail.html", {"news": news_item})
