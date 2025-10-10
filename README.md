## Единый адаптивный портал для повышения финансовой грамотности жителей Удмуртии: курсы, тесты, события, контакты, документы и отчёты — всё в одном месте. 

# Как запустить проект:

- Клонируйте репозиторий

git clone https://github.com/Ilushew/cyberforum.git
cd cyberforum

- Создайте виртуальное окружение

python -m venv .venv

source .venv/bin/activate  # Linux/macOS или .venv\Scripts\activate     # Windows

- Установите зависимости

pip install -r requirements.txt

- Запустите миграции

python manage.py migrate

- Cоздайте суперпользователя

python manage.py createsuperuser

- Запустите сервер

python manage.py runserver
