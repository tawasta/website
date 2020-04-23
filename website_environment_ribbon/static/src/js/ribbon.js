$( document ).ready(function () {
    var ribbon = $('<div class="test-ribbon hidden"/>');
    $('body').append(ribbon);
    ribbon.html("TEST");
    ribbon.css("height", "64px");
    ribbon.css("line-height", "40px");
});
