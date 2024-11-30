from django import forms
from django.core.exceptions import ValidationError

from code_review.extensions import all_extensions


def validate_file_extension(value):
    ext = value.name.split('.')[-1].lower()
    if f".{ext}" not in all_extensions:
        raise ValidationError(u'Неправильный формат файла')


def validate_zip_extension(value):
    ext = value.name.split('.')[-1].lower()
    if f".{ext}" not in ['.zip']:
        raise ValidationError(u'Неправильный формат файла')


class CodeUploadForm(forms.Form):
    code_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Вставьте код для анализа', 'id': 'code-editor'}),
        required=False,
        label='Текст кода'
    )
    code_file = forms.FileField(
        required=False,
        label='Загрузить файл с кодом', validators=[validate_file_extension]
    )
    code_archive = forms.FileField(
        required=False,
        label='Загрузить архив с кодом', validators=[validate_zip_extension]
    )
    github_link = forms.URLField(
        required=False,
        label='Ссылка на GitHub репозиторий'
    )
