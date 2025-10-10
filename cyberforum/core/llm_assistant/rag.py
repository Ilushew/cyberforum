from .model import llm
from .indexer import create_or_load_vectorstore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Промпт — лучше вынести сюда, чтобы легко менять
PROMPT_TEMPLATE = """
Вы — помощник, который отвечает на вопросы на основе предоставленного контекста.
Если в контексте нет информации, скажите: "Информация не найдена". Не воспринимай это слишком буквально - 
немного домысливать разумеется можно и нужно.  
(Учти, что этот текст будет отображаться на html странице, то есть например 
использовать ** и html-тэги для выделения текста жирным не получится. Лучше оставить текст 
без выделений, чем с непонятными символами)
Контекст:
{context}

Вопрос:
{question}

Ответ:
"""

prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
chain = prompt | llm | StrOutputParser()


def generate_answer(question: str, top_k: int = 3) -> str:
    """
    Генерирует ответ на вопрос с использованием RAG.
    Вызывается из Django view.
    """
    # Индекс уже должен быть загружен при старте сервера
    # Мы не пересоздаём его каждый раз!
    vectorstore = create_or_load_vectorstore()

    relevant_docs = vectorstore.similarity_search(question, k=top_k)

    context = "\n\n".join(
        [
            f"Источник: {doc.metadata['source']} (тип: {doc.metadata['file_type']})\n{doc.page_content}"
            for doc in relevant_docs
        ]
    )

    response = chain.invoke({"context": context, "question": question})

    return response
