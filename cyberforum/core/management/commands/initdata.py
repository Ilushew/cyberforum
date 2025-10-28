from django.core.management.base import BaseCommand

from core.models import Contact, Event
from courses.models import Course, Lesson, Question


class Command(BaseCommand):
    help = "Заполняет БД тестовыми данными"

    def handle(self, *args, **kwargs):
        # Очистка
        Contact.objects.all().delete()
        Event.objects.all().delete()
        Course.objects.all().delete()

        # Контакты
        Contact.objects.create(
            name="Центр финансовой грамотности Ижевск",
            address="ул. Пушкинская, 100",
            phone="+7 (3412) 12-34-56",
            audience="все",
        )

        # События
        from datetime import date

        Event.objects.create(
            title="День финансовой грамотности в школе №1",
            description="Открытый урок для школьников 8-11 классов",
            date=date(2025, 4, 20),
            location="Школа №1, Ижевск",
            audience="школьник",
        )

        # Курсы
        course1 = Course.objects.create(
            title="Семейный бюджет",
            description="Научитесь планировать доходы и расходы семьи.",
            audience="все",
            format_type="текст",
        )
        lesson1 = Lesson.objects.create(
            course=course1,
            title="Как составить бюджет",
            content="<p>Шаг 1: Учет всех доходов...</p>",
            video_url="https://www.youtube.com/embed/dQw4w9WgXcQ",
            order=1,
        )
        Question.objects.create(
            lesson=lesson1,
            text="Что входит в обязательные расходы?",
            option_a="Аренда жилья",
            option_b="Покупка нового телефона",
            option_c="Отпуск",
            correct_answer="A",
        )

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно загружены!"))
