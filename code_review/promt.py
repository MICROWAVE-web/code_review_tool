import tiktoken


# модели


def get_promt(code):
    promt_text = f"""
Проанализируй предоставленный код на соответствие следующим критериям:

Общие критерии:
1. Соответствие стандартам разработки, включая стиль кода, именование переменных, функций и классов.
2. Наличие документации и комментариев к методам, классам и сущностям.

(Если код написан на C#)
1. Проверь правильность использования NuGet пакетов, их обновление и отсутствие ненужных зависимостей.
2. Убедись, что архитектура соответствует стандартам IoC контейнеров, правильно зарегистрированы сервисы.
3. Использование LINQ и Entity Framework должно быть без ошибок, с оптимизированным кодом.
4. Нет ли ошибок, связанных с логированием, например, дублирования сообщений или неправильного объединения строк.

(Если код написан на TypeScript)
1. Соответствие проектной структуры и правил именования переменных, классов, методов.
2. Проверь использование рекомендуемых библиотек и методов.
3. Убедись, что код тестируется, нет уязвимостей, и соблюдены требования производительности.
4. Строки отформатированы, а стиль кода единообразен.

(Если код написан на Python)
1. Организация кода согласно принципам монорепозитория, наличие `.gitignore` и `.editorconfig`.
2. Использование поддерживаемых библиотек (например, Falcon, Gunicorn, Alembic) и модулей.
3. Логирование и мониторинг: использование `logging` для корректной записи логов.
4. Проверка безопасности: защита доступа, правильная обработка JWT токенов.
5. Соблюдение стандартов PEP8, PEP257 и наличие документации.

После анализа предоставь список найденных ошибок и рекомендаций по их исправлению. Если ошибок нет, напиши, что код соответствует всем критериям.

Внимание: итоговый ответ должен быть содержательным, по возможности, содержать участки проблемные кода или хотя бы файл и строчку с проблемой, должен быть написан на русском языке и укладываться в 800 токена.


Данные для анализа:
{code}
"""
    tokens = count_tokens(promt_text)

    max_tokens = 4000
    token_warning = False

    if tokens > max_tokens:
        k = max_tokens / tokens
        promt_text = promt_text[:int(len(promt_text) * k)]
        token_warning = True

    return token_warning, promt_text


def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Примерное вычисление токенов для текста, для вычисления будем использовать модель gpt-3.5-turbo
    P.S. Это не использование самой нейросети, а лишь вычисление примерного количества токенов для запроса в ЕвразGPT
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
