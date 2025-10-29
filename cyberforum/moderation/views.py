import moderation.forms
import core.telegram_utils
import core.views
import courses.models
import documentation.forms
import documentation.models
import events.forms
import events.models
import news.forms
import news.models

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect


@user_passes_test(core.views.is_moderator, login_url="/login/")
def documentation_moderator_list(request):
    docs = documentation.models.DocumentationFile.objects.all().order_by("-uploaded_at")
    return render(
        request, "moderation/documentation_moderator_list.html", {"docs": docs}
    )


@user_passes_test(core.views.core.views.is_moderator, login_url="/login/")
def documentation_create(request):
    if request.method == "POST":
        form = documentation.forms.DocumentationFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Документ успешно загружен!")
            return redirect("moderation:documentation_list")
    else:
        form = documentation.forms.DocumentationFileForm()
    return render(
        request,
        "moderation/documentation_form.html",
        {"form": form, "title": "Загрузить документ"},
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def documentation_delete(request, doc_id):
    doc = get_object_or_404(documentation.models.DocumentationFile, id=doc_id)
    if request.method == "POST":
        doc.delete()
        messages.success(request, "Документ удалён.")
        return redirect("moderation:documentation_list")
    return render(request, "moderation/documentation_confirm_delete.html", {"doc": doc})


@user_passes_test(core.views.is_moderator, login_url="/login/")
def event_moderator_list(request):
    Events = events.models.Event.objects.all().order_by("date")
    return render(
        request, "moderation/event_moderator_list.html", {"event_list": Events}
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def event_create(request):
    if request.method == "POST":
        form = events.forms.EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, "Событие успешно создано!")

            msg = (
                "📢 <b>Новое событие!</b>\n"
                f"<b>{event.title}</b>\n"
                f"📅 Дата: {event.date.strftime('%d.%m.%Y')}\n"
                f"📍 Место: {event.location}\n"
                f"👥 Аудитория: {event.get_audience_display()}\n"
                f"{event.description[:200]}{'...' if len(event.description) > 200 else ''}"
            )
            core.telegram_utils.send_telegram_message(msg)

            return redirect("moderation:event_list")
    else:
        form = events.forms.EventForm()
    return render(
        request, "moderation/event_form.html", {"form": form, "title": "Создать событие"}
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def event_edit(request, event_id):
    event = get_object_or_404(events.models.Event, id=event_id)
    if request.method == "POST":
        form = events.forms.EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Событие успешно обновлено!")
            return redirect("moderation:event_list")
    else:
        form = events.forms.EventForm(instance=event)
    return render(
        request,
        "moderation/event_form.html",
        {"form": form, "title": "Редактировать событие"},
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def event_delete(request, event_id):
    event = get_object_or_404(events.models.Event, id=event_id)
    if request.method == "POST":
        event.delete()
        messages.success(request, "Событие удалено.")
        return redirect("moderation:event_list")
    return render(request, "moderation/event_confirm_delete.html", {"event": event})



@user_passes_test(core.views.is_moderator, login_url="/login/")
def news_moderator_list(request):
    news_items = news.models.News.objects.all().order_by("-created_at")
    return render(
        request, "moderation/news_moderator_list.html", {"news_list": news_items}
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def news_create(request):
    if request.method == "POST":
        form = news.forms.NewsForm(request.POST, request.FILES)  # ← request.FILES
        if form.is_valid():
            News = form.save(commit=False)
            News.author = request.user
            News.save()
            messages.success(request, "Новость успешно создана!")

            if News.is_published:
                msg = (
                    "📰 <b>Новая новость!</b>\n"
                    f"<b>{News.title}</b>\n"
                    f"{News.content[:200]}{'...' if len(News.content) > 200 else ''}"
                )
                core.telegram_utils.send_telegram_message(msg)

            return redirect("moderation:news_list")
    else:
        form = news.forms.NewsForm()
    return render(
        request, "moderation/news_form.html", {"form": form, "title": "Создать новость"}
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def news_edit(request, news_id):
    News = get_object_or_404(news.models.News, id=news_id)
    if request.method == "POST":
        form = news.forms.NewsForm(request.POST, request.FILES, instance=News)  # ← request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Новость успешно обновлена!")
            return redirect("moderation:news_list")
    else:
        form = news.forms.NewsForm(instance=News)
    return render(
        request,
        "moderation/news_form.html",
        {"form": form, "title": "Редактировать новость"},
    )


@user_passes_test(core.views.is_moderator, login_url="/login/")
def news_delete(request, news_id):
    News = get_object_or_404(news.models.News, id=news_id)
    if request.method == "POST":
        News.delete()
        messages.success(request, "Новость удалена.")
        return redirect("moderation:news_list")
    return render(request, "moderation/news_confirm_delete.html", {"news": News})


@user_passes_test(core.views.is_moderator, login_url="/login/")
def dashboard(request):
    return render(request, "moderation/dashboard.html")


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_moderator_list(request):
    Courses = courses.models.Course.objects.all().order_by('-created_at')
    return render(request, 'moderation/course_moderator_list.html', {'courses': Courses})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_create(request):
    if request.method == 'POST':
        form = moderation.forms.CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Курс успешно создан!")
            return redirect('moderation:course_moderator_list')
    else:
        form = moderation.forms.CourseForm()
    return render(request, 'moderation/course_form.html', {'form': form, 'title': 'Создать курс'})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_edit(request, course_id):
    course = get_object_or_404(courses.models.Course, id=course_id)
    if request.method == 'POST':
        form = moderation.forms.CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Курс обновлён!")
            return redirect('moderation:course_moderator_list')
    else:
        form = moderation.forms.CourseForm(instance=course)
    return render(request, 'moderation/course_form.html', {'form': form, 'title': 'Редактировать курс'})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_delete(request, course_id):
    course = get_object_or_404(courses.models.Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Курс удалён.")
        return redirect('moderation:course_moderator_list')
    return render(request, 'moderation/course_confirm_delete.html', {'course': course})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_list(request, course_id):
    course = get_object_or_404(courses.models.Course, id=course_id)
    lessons = course.lessons.all().order_by('order')
    return render(request, 'moderation/lesson_list.html', {
        'course': course,
        'lessons': lessons
    })


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_create(request, course_id):
    course = get_object_or_404(courses.models.Course, id=course_id)
    if request.method == 'POST':
        lesson_form = moderation.forms.LessonForm(request.POST)
        question_formset = moderation.forms.QuestionFormSet(request.POST)
        if lesson_form.is_valid() and question_formset.is_valid():
            lesson = lesson_form.save(commit=False)
            lesson.course = course
            lesson.save()
            question_formset.instance = lesson
            question_formset.save()
            messages.success(request, "Урок успешно создан!")
            return redirect('moderation:lesson_list', course_id=course.id)
    else:
        lesson_form = moderation.forms.LessonForm()
        question_formset = moderation.forms.QuestionFormSet()
    return render(request, 'moderation/lesson_form.html', {
        'form': lesson_form,
        'formset': question_formset,
        'course': course,
        'title': 'Создать урок'
    })


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(courses.models.Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson_form = moderation.forms.LessonForm(request.POST, instance=lesson)
        question_formset = moderation.forms.QuestionFormSet(request.POST, instance=lesson)
        if lesson_form.is_valid() and question_formset.is_valid():
            lesson_form.save()
            question_formset.save()
            messages.success(request, "Урок обновлён!")
            return redirect('moderation:lesson_list', course_id=lesson.course.id)
    else:
        lesson_form = moderation.forms.LessonForm(instance=lesson)
        question_formset = moderation.forms.QuestionFormSet(instance=lesson)
    return render(request, 'moderation/lesson_form.html', {
        'form': lesson_form,
        'formset': question_formset,
        'course': lesson.course,
        'title': 'Редактировать урок'
    })


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(courses.models.Lesson, id=lesson_id)
    course_id = lesson.course.id
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Урок удалён.")
        return redirect('moderation:lesson_list', course_id=course_id)
    return render(request, 'moderation/lesson_confirm_delete.html', {'lesson': lesson})
