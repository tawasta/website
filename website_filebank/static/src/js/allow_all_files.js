//Change filebank upload form to accept all kinds of files
$( document ).ready(function() {
    $( "a.btn" ).click(function() {
        setTimeout(function() {
            $("input").each(function() {
                $(this).attr("accept", "*");
            });
        }, 1000);
    });
});
