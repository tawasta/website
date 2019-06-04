console.log("hello");
$( document ).ready(function() {
    $( "a.btn" ).click(function() {
        console.log("lol");
        setTimeout(function() {
        $("input").each(function() {
                $(this).attr("accept", "*");
        });
        }, 1000);
    });
});
