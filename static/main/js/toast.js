function showToast(message, type = 'info') {
    const toastEl = document.getElementById('loadingToast');
    const toastBody = toastEl.querySelector('.toast-body');

    // Удаляем предыдущие классы фона
    toastEl.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-dark');

    // Добавляем нужный класс в зависимости от типа
    const bgClass = {
        success: 'bg-success',
        error: 'bg-danger',
        warning: 'bg-warning',
        info: 'bg-info',
    }[type] || 'bg-dark'; // По умолчанию bg-dark
    toastEl.classList.add(bgClass);

    // Устанавливаем текст и показываем Toast
    toastBody.textContent = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}
