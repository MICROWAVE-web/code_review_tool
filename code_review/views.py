from django.shortcuts import render

# Create your views here.

import os
import markdown
from django.shortcuts import render
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from .forms import CodeUploadForm

def analyze_code(code_input):
    """
    Заглушка для анализа кода
    В реальном приложении здесь будет логика анализа
    """
    return """
# Отчет по анализу кода

## Общая статистика
- Количество строк: 100
- Сложность: Средняя
- Стиль кода: Требует улучшения

## Рекомендации
1. Используйте более понятные имена переменных
2. Разбейте длинные функции на smaller функции
3. Добавьте комментарии к сложным участкам кода
"""

def generate_pdf_report(markdown_text):
    """Генерация PDF из Markdown"""
    pdf_path = 'code_review_report.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    html = markdown.markdown(markdown_text)
    
    # Здесь можно добавить более сложную конвертацию HTML в PDF
    with open(pdf_path, 'wb') as f:
        c = canvas.Canvas(f, pagesize=letter)
        c.drawString(100, 750, "Отчет по анализу кода")
        c.drawString(100, 700, markdown_text)
        c.save()
    
    return pdf_path

def code_review_view(request):
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
                # Обработка архива (заглушка)
                analysis_result = "Архив загружен, но анализ не реализован"
            elif github_link:
                # Обработка GitHub ссылки (заглушка)
                analysis_result = "GitHub репозиторий получен, но анализ не реализован"
            else:
                analysis_result = "Нет данных для анализа"

            # Генерация PDF
            pdf_path = generate_pdf_report(analysis_result)

            with open(pdf_path, 'rb') as pdf:
                response = FileResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'inline; filename="code_review_report.pdf"'
                return response

    else:
        form = CodeUploadForm()
    
    return render(request, 'code_review/upload.html', {'form': form})
