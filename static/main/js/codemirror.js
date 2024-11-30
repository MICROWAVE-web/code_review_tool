document.addEventListener("DOMContentLoaded", () => {
    const defaultText = `# Пример кода для анализа:
def calculate_sum(arr):

    sum = 0
    for i in range(len(arr)):
        sum += arr[i]
    return sum

result = calculate_sum([1, 2, 3, 4, 5])
print(results)`;
    const textarea = document.getElementById("code-editor");
    textarea.value = defaultText; // Заполняем текстом по умолчанию
    const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
        lineNumbers: true, // Номера строк
        mode: "javascript", // Язык подсветки
        theme: "darcula",   // Тема подсветки
        tabSize: 2          // Размер табуляции
    });
    // Увеличиваем высоту редактора
    editor.setSize(null, "500px"); // Ширина (null означает автоматическую) и высота
});