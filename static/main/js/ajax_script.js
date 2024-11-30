function submitForm(formId) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Показываем Toast перед отправкой
    showToast('Обработка...', 'default');

    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) {
                console.log(response);
                showToast(response.message, 'error');
            }
            console.log(response);
            return response.json(); // Получаем JSON
        })
        .then(data => {
            // Показать сообщение из ответа в Toast
            if (data.status === 'success') {
                showToast(data.message, 'success');
            } else if (data.status === 'warning') {
                showToast(data.message, 'warning');
            } else if (data.status === 'error') {
                console.log(data)
                showToast(data.message, 'error');
                return
            }

            // Декодируем Base64 в бинарные данные
            const binaryString = atob(data.file_content);
            const binaryLen = binaryString.length;
            const bytes = new Uint8Array(binaryLen);
            for (let i = 0; i < binaryLen; i++) {
                bytes[i] = binaryString.charCodeAt(i);
            }

            // Создаем Blob и скачиваем файл
            const blob = new Blob([bytes], {type: 'application/pdf'});
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = data.file_name; // Имя файла из ответа
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .catch(error => {
            // Обработка ошибок, отображаем сообщение об ошибке в Toast
            showToast("Неизвестная ошибка", 'error');
            console.error(error);
        });
}
