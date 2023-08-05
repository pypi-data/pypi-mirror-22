$(function () {
    $(".editors textarea").each(function () {
        var myCodeMirror = CodeMirror.fromTextArea(this, {
            lineNumbers: true,
            mode: "lua",
        });
    })
});