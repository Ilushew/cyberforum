from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    TextLoader,
    PyMuPDFLoader,
    Docx2txtLoader,
)

SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx"}

def load_documents_from_folder(folder_path: str) -> List:
    documents = []
    folder = Path(folder_path)
    if not folder.exists():
        raise FileNotFoundError(f"Папка {folder_path} не найдена!")

    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            print(f"📄 Загружаю: {file_path.name}")
            if file_path.suffix.lower() == ".txt":
                loader = TextLoader(file_path, encoding="utf-8")
            elif file_path.suffix.lower() == ".pdf":
                loader = PyMuPDFLoader(file_path)
            elif file_path.suffix.lower() == ".docx":
                loader = Docx2txtLoader(file_path)
            else:
                continue

            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = file_path.name
                doc.metadata["file_type"] = file_path.suffix.lower()[1:]
            documents.extend(docs)

    if not documents:
        print("⚠️  В папке docs не найдено ни одного поддерживаемого файла (.txt, .pdf, .docx)")
    else:
        print(f"✅ Успешно загружено {len(documents)} документов.")

    return documents