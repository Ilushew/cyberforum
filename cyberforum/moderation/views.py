from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect

from core.views import is_moderator
from documentation.forms import DocumentationFileForm
from documentation.models import DocumentationFile
from django.contrib import messages

from events.forms import EventForm
from events.models import Event
from news.forms import NewsForm
from news.models import News


@user_passes_test(is_moderator, login_url="/login/")
def documentation_moderator_list(request):
    docs = DocumentationFile.objects.all().order_by("-uploaded_at")
    return render(
        request, "moderation/documentation_moderator_list.html", {"docs": docs}
    )


@user_passes_test(is_moderator, login_url="/login/")
def documentation_create(request):
    if request.method == "POST":
        form = DocumentationFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Документ успешно загружен!")
            return redirect("moderation:documentation_list")
    else:
        form = DocumentationFileForm()
    return render(
        request,
        "moderation/documentation_form.html",
        {"form": form, "title": "Загрузить документ"},
    )


@user_passes_test(is_moderator, login_url="/login/")
def documentation_delete(request, doc_id):
    doc = get_object_or_404(DocumentationFile, id=doc_id)
    if request.method == "POST":
        doc.delete()
        messages.success(request, "Документ удалён.")
        return redirect("moderation:documentation_list")
    return render(request, "moderation/documentation_confirm_delete.html", {"doc": doc})


@user_passes_test(is_moderator, login_url="/login/")
def event_moderator_list(request):
    events = Event.objects.all().order_by("date")
    return render(
        request, "moderation/event_moderator_list.html", {"event_list": events}
    )


@user_passes_test(is_moderator, login_url="/login/")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Событие успешно создано!")
            return redirect("moderation:event_list")
    else:
        form = EventForm()
    return render(
        request,
        "moderation/event_form.html",
        {"form": form, "title": "Создать событие"},
    )


@user_passes_test(is_moderator, login_url="/login/")
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Событие успешно обновлено!")
            return redirect("moderation:event_list")
    else:
        form = EventForm(instance=event)
    return render(
        request,
        "moderation/event_form.html",
        {"form": form, "title": "Редактировать событие"},
    )


@user_passes_test(is_moderator, login_url="/login/")
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Событие удалено.")
        return redirect("moderation:event_list")
    return render(request, "moderation/event_confirm_delete.html", {"event": event})


@user_passes_test(is_moderator, login_url="/login/")
def news_moderator_list(request):
    news_items = News.objects.all().order_by("-created_at")
    return render(
        request, "moderation/news_moderator_list.html", {"news_list": news_items}
    )


@user_passes_test(is_moderator, login_url="/login/")
def news_create(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)  # ← request.FILES
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            messages.success(request, "Новость успешно создана!")
            return redirect("moderation:news_list")
    else:
        form = NewsForm()
    return render(
        request, "moderation/news_form.html", {"form": form, "title": "Создать новость"}
    )


@user_passes_test(is_moderator, login_url="/login/")
def news_edit(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)  # ← request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Новость успешно обновлена!")
            return redirect("moderation:news_list")
    else:
        form = NewsForm(instance=news)
    return render(
        request,
        "moderation/news_form.html",
        {"form": form, "title": "Редактировать новость"},
    )


@user_passes_test(is_moderator, login_url="/login/")
def news_delete(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        news.delete()
        messages.success(request, "Новость удалена.")
        return redirect("moderation:news_list")
    return render(request, "moderation/news_confirm_delete.html", {"news": news})


@user_passes_test(is_moderator, login_url="/login/")
def dashboard(request):
    return render(request, "moderation/dashboard.html")
