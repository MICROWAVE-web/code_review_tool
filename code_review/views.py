# Create your views here.
import io
import zipfile
from io import BytesIO
import os
import tempfile
import git
import markdown_pdf
from django.http import FileResponse, HttpRequest
from django.shortcuts import render

from .extensions import all_extensions
from .forms import CodeUploadForm


def analyze_code(code_input):
    """
    Заглушка для анализа кода
    В реальном приложении здесь будет логика анализа
    """
    return f"""
# Отчет по анализу кода

## Общая статистика
- Количество строк: 100
- Сложность: Средняя
- Стиль кода: Требует улучшения

## Рекомендации
1. Используйте более понятные имена переменных
2. Разбейте длинные функции на smaller функции
3. Добавьте комментарии к сложным участкам кода

{code_input}
"""


def generate_pdf_report(markdown_text, output_path="report.pdf"):
    """
    Генерация PDF из текста в формате Markdown с использованием markdown-pdf.

    Args:
        markdown_text (str): Текст в формате Markdown.
        output_path (str): Путь для сохранения PDF.

    Returns:
        Buffer: Данные PDF-файла.
    """

    # Преобразуем Markdown в PDF
    pdf = markdown_pdf.MarkdownPdf()
    pdf.add_section(markdown_pdf.Section(markdown_text, toc=False))
    pdf.meta["title"] = "User Guide"
    pdf.meta["author"] = "Vitaly Bogomolov"
    pdf.writer.close()
    return pdf.out_file.getvalue()


def process_archive(archive_file, allowed_extensions=None):
    """
    Обработка архива: чтение содержимого файлов с определенными расширениями.

    Args:
        archive_file (UploadedFile): Загруженный архив.
        allowed_extensions (list[str]): Список разрешенных расширений (например, ['.py', '.txt']).

    Returns:
        str: Содержимое файлов с их относительными путями.
    """
    if allowed_extensions is None:
        allowed_extensions = all_extensions  # Разрешенные расширения по умолчанию

    result_content = ""

    with zipfile.ZipFile(archive_file) as archive:
        for file_name in archive.namelist():
            # Проверяем, является ли файл допустимого типа
            if any(file_name.endswith(ext) for ext in allowed_extensions):
                with archive.open(file_name) as file:
                    try:
                        # Читаем содержимое файла
                        file_content = file.read().decode('utf-8')
                        # Добавляем путь к файлу и его содержимое в результат
                        result_content += f"### File: {file_name}\n{file_content}\n\n"
                    except UnicodeDecodeError:
                        result_content += f"### File: {file_name}\n[Не удалось прочитать файл]\n\n"
    return result_content


def process_github_repo(github_link):
    """
    Клонирует репозиторий, извлекает файлы с указанными расширениями и объединяет их содержимое.

    :param github_link: Ссылка на git-репозиторий
    :param file_extensions: список допустимых расширений файлов (например, ['.py', '.txt'])
    :return: строка, содержащая содержимое всех файлов с указанными расширениями
             с указанием их относительного пути
    """
    try:
        # Создаем временную директорию для клонирования репозитория
        with tempfile.TemporaryDirectory() as temp_dir:
            # Клонируем репозиторий
            repo = git.Repo.clone_from(github_link, temp_dir)

            # Переменная для накопления результата
            collected_text = []

            # Перебираем все файлы в репозитории
            for root, _, files in os.walk(temp_dir):
                for file_name in files:
                    # Проверяем расширение файла
                    if any(file_name.endswith(ext) for ext in all_extensions):
                        # Относительный путь к файлу
                        relative_path = os.path.relpath(os.path.join(root, file_name), temp_dir)
                        # Чтение содержимого файла
                        with open(os.path.join(root, file_name), 'r', encoding='utf-8') as file:
                            file_content = file.read()
                        # Добавляем путь и содержимое в результирующую переменную
                        collected_text.append(f"### {relative_path}\n{file_content}\n")

            return "\n".join(collected_text)

    except git.exc.GitError as e:
        return f"Ошибка работы с git: {str(e)}"
    except Exception as e:
        return f"Общая ошибка: {str(e)}"


def code_review_view(request: HttpRequest):
    if request.method == 'POST':
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            code_text = form.cleaned_data['code_text']
            code_file = form.cleaned_data['code_file']
            code_archive = form.cleaned_data['code_archive']
            github_link = form.cleaned_data['github_link']

            # Логика обработки входных данных
            if code_text:
                analysis_result = analyze_code(code_text)
            elif code_file:
                # Чтение файла
                code_text = code_file.read().decode('utf-8')
                analysis_result = analyze_code(code_text)
            elif code_archive:
                # Обработка архива
                text_to_analyse = process_archive(code_archive)
                analysis_result = analyze_code(text_to_analyse)
            elif github_link:
                # Обработка GitHub ссылки (заглушка)
                text_to_analyse = process_github_repo(github_link)
                analysis_result = analyze_code(text_to_analyse)
            else:
                analysis_result = "Нет данных для анализа"

            # Генерация PDF
            data = generate_pdf_report(analysis_result, 'reports/report.pdf')
            buf = BytesIO(data)
            buf.seek(io.SEEK_SET)
            response = FileResponse(
                buf,
                as_attachment=True,
                filename="report.pdf",
            )
            return response
    else:
        form = CodeUploadForm()

    return render(request, 'code_review/upload.html', {'form': form})
