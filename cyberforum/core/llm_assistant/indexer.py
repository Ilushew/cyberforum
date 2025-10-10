import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .loader import load_documents_from_folder
from .utils import clean_text, count_tokens

INDEX_DIR = "faiss_index"

CURRENT_DIR = Path(__file__).parent
DOCS_DIR = CURRENT_DIR / "docs"


def create_or_load_vectorstore():
    """
    Создаёт или загружает векторную базу.
    Вызывается один раз при запуске Django.
    """
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    if os.path.exists(INDEX_DIR):
        print("🔄 Загрузка существующего индекса...")
        vectorstore = FAISS.load_local(
            INDEX_DIR, embedding_model, allow_dangerous_deserialization=True
        )
        print("✅ Индекс загружен.")
    else:
        print("🆕 Создание нового индекса...")
        documents = load_documents_from_folder(DOCS_DIR)
        if not documents:
            raise RuntimeError("Нет документов для индексации!")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=45,
            chunk_overlap=35,
            length_function=count_tokens,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        )

        chunks = splitter.split_documents(documents)
        for chunk in chunks:
            chunk.page_content = clean_text(chunk.page_content)

        vectorstore = FAISS.from_documents(chunks, embedding_model)
        vectorstore.save_local(INDEX_DIR)
        print(f"✅ Индекс сохранён в {INDEX_DIR}/")

    return vectorstore
