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

from courses.models import Course
from moderation.forms import CourseForm
from courses.models import Lesson, Question
from .forms import LessonForm, QuestionFormSet


@user_passes_test(is_moderator, login_url="/login/")
def documentation_moderator_list(request):
    docs = DocumentationFile.objects.all().order_by("-uploaded_at")
    return render(request, "moderation/documentation_moderator_list.html", {"docs": docs})


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
    return render(request, "moderation/event_moderator_list.html", {"event_list": events})


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
        request, "moderation/event_form.html", {"form": form, "title": "Создать событие"}
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
    return render(request, "moderation/event_confirm_delete.html", {"event": event}) \
 \
 \
@user_passes_test(is_moderator, login_url="/login/")
def news_moderator_list(request):
    news_items = News.objects.all().order_by("-created_at")
    return render(request, "moderation/news_moderator_list.html", {"news_list": news_items})


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
        request, "moderation/news_form.html", {"form": form, "title": "Редактировать новость"}
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


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_moderator_list(request):
    courses = Course.objects.all().order_by('-created_at')
    return render(request, 'moderation/course_moderator_list.html', {'courses': courses})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Курс успешно создан!")
            return redirect('moderation:course_moderator_list')
    else:
        form = CourseForm()
    return render(request, 'moderation/course_form.html', {'form': form, 'title': 'Создать курс'})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Курс обновлён!")
            return redirect('moderation:course_moderator_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'moderation/course_form.html', {'form': form, 'title': 'Редактировать курс'})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def course_delete(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        course.delete()
        messages.success(request, "Курс удалён.")
        return redirect('moderation:course_moderator_list')
    return render(request, 'moderation/course_confirm_delete.html', {'course': course})


@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_list(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all().order_by('order')
    return render(request, 'moderation/lesson_list.html', {
        'course': course,
        'lessons': lessons
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        if lesson_form.is_valid() and question_formset.is_valid():
            lesson = lesson_form.save(commit=False)
            lesson.course = course
            lesson.save()
            question_formset.instance = lesson
            question_formset.save()
            messages.success(request, "Урок успешно создан!")
            return redirect('moderation:lesson_list', course_id=course.id)
    else:
        lesson_form = LessonForm()
        question_formset = QuestionFormSet()
    return render(request, 'moderation/lesson_form.html', {
        'form': lesson_form,
        'formset': question_formset,
        'course': course,
        'title': 'Создать урок'
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_edit(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson_form = LessonForm(request.POST, instance=lesson)
        question_formset = QuestionFormSet(request.POST, instance=lesson)
        if lesson_form.is_valid() and question_formset.is_valid():
            lesson_form.save()
            question_formset.save()
            messages.success(request, "Урок обновлён!")
            return redirect('moderation:lesson_list', course_id=lesson.course.id)
    else:
        lesson_form = LessonForm(instance=lesson)
        question_formset = QuestionFormSet(instance=lesson)
    return render(request, 'moderation/lesson_form.html', {
        'form': lesson_form,
        'formset': question_formset,
        'course': lesson.course,
        'title': 'Редактировать урок'
    })

@user_passes_test(lambda u: u.is_authenticated and u.is_moderator, login_url='/login/')
def lesson_delete(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Урок удалён.")
        return redirect('moderation:lesson_list', course_id=course_id)
    return render(request, 'moderation/lesson_confirm_delete.html', {'lesson': lesson})