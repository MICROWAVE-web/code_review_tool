document.addEventListener("DOMContentLoaded", () => {
    const editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
        lineNumbers: true, // Номера строк
        mode: "javascript", // Язык подсветки
        theme: "darcula",   // Тема подсветки
        tabSize: 2          // Размер табуляции
    });
});