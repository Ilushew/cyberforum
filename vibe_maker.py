import os
import sys
from pathlib import Path

"""
Просто запускай как обычный файл .py. Создаст текстовый файл, 
содержимое которого можно отправить LLM как контекст проекта  
"""
def is_text_file(file_path):
    """Проверяет, является ли файл текстовым (не бинарным)"""
    text_extensions = {
        '.py', '.txt', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.js',
        '.ini', '.cfg', '.toml', '.env', '.log', '.sql', '.csv', '.bat', '.sh', '.rst'
    }
    return file_path.suffix.lower() in text_extensions or file_path.name.endswith('.gitignore')


def export_project_structure(root_dir, output_file="project_structure.txt"):
    """
    Экспортирует структуру проекта и содержимое файлов в текстовый файл.
    """
    root_path = Path(root_dir)
    if not root_path.exists() or not root_path.is_dir():
        print(f"❌ Ошибка: Папка '{root_dir}' не существует или не является директорией.")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== СТРУКТУРА ПРОЕКТА: {root_path.name} ===\n")
        f.write(f"Путь: {root_path.absolute()}\n")
        f.write("=" * 60 + "\n\n")

        def write_tree(path, indent=""):
            items = sorted(path.iterdir())  # Сортируем для стабильности
            for item in items:
                rel_path = item.relative_to(root_path)
                if item.is_dir():
                    f.write(f"{indent}📁 {item.name}/\n")
                    write_tree(item, indent + "  ")
                elif item.is_file():
                    # Проверяем, текстовый ли файл
                    if is_text_file(item):
                        f.write(f"{indent}📄 {item.name}\n")
                        try:
                            content = item.read_text(encoding='utf-8')
                            f.write(f"{indent}    --- СОДЕРЖИМОЕ ---\n")
                            for line in content.splitlines():
                                f.write(f"{indent}    {line}\n")
                            f.write(f"{indent}    --- КОНЕЦ ---\n\n")
                        except UnicodeDecodeError:
                            f.write(f"{indent}    ❗ Не удалось прочитать (неподдерживаемая кодировка)\n\n")
                    else:
                        # Не текстовый файл — просто упоминаем
                        f.write(f"{indent}📄 {item.name} (бинарный, пропущен)\n")

        write_tree(root_path)

    print(f"✅ Успешно! Структура проекта сохранена в файл: {output_file}")


if __name__ == "__main__":
    # Если путь не передан — используем текущую директорию
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "."
    export_project_structure(folder_path)
