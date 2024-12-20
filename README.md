# Инструмент Анализа Кода

## Описание
Веб-приложение для автоматизированного анализа программного кода, разработанное для оптимизации процесса code review в крупных компаниях.

## Возможности
- Загрузка кода через текстовое поле
- Загрузка отдельных файлов с кодом
- Загрузка архивов с кодом
- Поддержка ссылок на GitHub репозитории
- Генерация PDF-отчета с анализом кода

## Установка
1. Клонируйте репозиторий
2. Создайте виртуальное окружение
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
venv\Scripts\activate     # Для Windows
```

3. Установите зависимости
```bash
pip install -r requirements.txt
```

4. Запустите миграции
```bash
python manage.py migrate
```

5. Запустите сервер
```bash
python manage.py runserver
```

## Технологии
- Django
- Markdown
- ReportLab
- PyGithub
