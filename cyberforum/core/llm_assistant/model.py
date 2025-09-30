import os
from langchain_gigachat.chat_models import GigaChat

# Установите ключ в .env или здесь (лучше через .env)
os.environ["GIGACHAT_CREDENTIALS"] = "NGRiZjA5MmMtYmJkOS00NzkzLWJlZGQtM2UzYWFlZTNiNWMwOjlmMjQ0MjU5LWUxM2YtNGUyYy1iYTg1LWFlOTlhZDhjMWUzOQ=="

llm = GigaChat(
    model="GigaChat-Pro",
    verify_ssl_certs=False,
    timeout=60
)