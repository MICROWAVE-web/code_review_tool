# Create your views here.
import base64
import io
import json
import os
import tempfile
import zipfile
from io import BytesIO

import git
import markdown_pdf
import requests
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from code_review_tool import settings
from .extensions import all_extensions
from .forms import CodeUploadForm
from .promt import get_promt

# Конфигурация API
API_URL = "http://84.201.152.196:8020/v1/completions"
API_KEY = settings.CODE_REVIEW_API_KEY


def analyze_code(code_text):
    """
    Отправляет текст кода в Mistral-Nemo-Instruct для анализа.
    """
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    token_warning, promt = get_promt(code_text)

    payload = {
        "model": "mistral-nemo-instruct-2407",
        "messages": [
            {"role": "system",
             "content": "Ты ассистент, который говорит исключительно на русском языке. Никогда не используй английский язык, даже в примерах кода."},
            {"role": "user", "content": promt}
        ],
        "max_tokens": 1023,
        "temperature": 0.22
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.encoding = 'utf-8'
        if response.status_code == 200:
            data = response.json()
            return token_warning, data["choices"][0]["message"]["content"]
        elif response.status_code == 422:
            error_data = response.json()  # Декодируем JSON
            error_message = error_data.get('error', {}).get('message', 'Неизвестная ошибка')
            return token_warning, f"Ошибка: {response.status_code} - {error_message}"
        else:
            return token_warning, f"Ошибка: {response.status_code} - {response.text}"
    except Exception as e:
        return token_warning, f"Ошибка при подключении к серверу: {e}"


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
                        result_content += f"### Файл: {file_name}\n{file_content}\n\n"
                    except UnicodeDecodeError:
                        result_content += f"### Файл: {file_name}\n[Не удалось прочитать файл]\n\n"
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
                        collected_text.append(f"### Файл: {relative_path}\n{file_content}\n")

            return "\n".join(collected_text)

    except git.exc.GitError as e:
        return f"Ошибка работы с git: {str(e)}"
    except Exception as e:
        return f"Общая ошибка: {str(e)}"


def main_view(request):
    if request.method == "POST":
        form = CodeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                code_text = form.cleaned_data['code_text']
                code_file = form.cleaned_data['code_file']
                code_archive = form.cleaned_data['code_archive']
                github_link = form.cleaned_data['github_link']

                # Логика обработки входных данных
                if code_text:
                    token_warning, analysis_result = analyze_code(code_text)
                elif code_file:
                    # Чтение файла
                    code_text = code_file.read().decode('utf-8')
                    token_warning, analysis_result = analyze_code(code_text)
                elif code_archive:
                    # Обработка архива
                    text_to_analyse = process_archive(code_archive)
                    token_warning, analysis_result = analyze_code(text_to_analyse)
                elif github_link:
                    # Обработка GitHub ссылки
                    text_to_analyse = process_github_repo(github_link)
                    token_warning, analysis_result = analyze_code(text_to_analyse)
                else:
                    token_warning = False
                    analysis_result = "Нет данных для анализа"

                # Генерация PDF
                data = generate_pdf_report(analysis_result, 'reports/report.pdf')
                buf = BytesIO(data)
                buf.seek(io.SEEK_SET)

                # Кодируем файл в Base64
                base64_file = base64.b64encode(buf.read()).decode('utf-8')

                if not token_warning:
                    return JsonResponse({
                        "message": "Отчет успешно создан!",
                        "status": "success",
                        "file_name": "report.pdf",
                        "file_content": base64_file,
                    })
                else:
                    return JsonResponse({
                        "message": "Внимание! Код, предложенный для анализа слишком большой поэтому ответ может быть "
                                   "неполным ",
                        "status": "warning",
                        "file_name": "report.pdf",
                        "file_content": base64_file,
                    })
            except Exception as e:
                return JsonResponse({
                    "message": f"Произошла ошибка: {e}",
                    "status": "error",
                    "file_name": "report.pdf",
                })
        else:
            return JsonResponse({'message': 'Ошибка', 'errors': form.errors}, status=400)
    else:
        form = CodeUploadForm()
        return render(request, 'code_review/upload.html', {'form': form})


def result_view(request: HttpRequest):
    return render(request, 'code_review/result.html', )
