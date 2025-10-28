import re

from bs4 import BeautifulSoup


def clean_text(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\u200b-\u200d\uFEFF]", "", text)
    text = re.sub(r"страниц[а-ы]?\s*\d+\s*из\s*\d+", "", text, flags=re.IGNORECASE)
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^\w\s.,!?;:()\-\–—\"\'\n]", " ", text)
    return text.strip()


# Используем ту же кодировку, что и у GigaChat (GPT-4)
try:
    import tiktoken

    encoder = tiktoken.encoding_for_model("gpt-4")
except ImportError:
    encoder = None


def count_tokens(text: str) -> int:
    if encoder is None:
        return len(text.split()) * 1.3  # Приблизительно
    return len(encoder.encode(text))
