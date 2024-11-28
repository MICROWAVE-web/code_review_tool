from django import forms

class CodeUploadForm(forms.Form):
    code_text = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Вставьте код для анализа'}), 
        required=False, 
        label='Текст кода'
    )
    code_file = forms.FileField(
        required=False, 
        label='Загрузить файл с кодом'
    )
    code_archive = forms.FileField(
        required=False, 
        label='Загрузить архив с кодом'
    )
    github_link = forms.URLField(
        required=False, 
        label='Ссылка на GitHub репозиторий'
    )
