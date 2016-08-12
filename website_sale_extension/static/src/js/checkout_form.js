jQuery(document).ready(function ($) {

    // Automatically format the name field
    $("#forename_input").keyup(function(){
        updateName();
    });
    $("#surname_input").keyup(function(){
        updateName();
    });

    function updateName(){
        var full_name = $("#forename_input").val() + " " + $("#surname_input").val()

        $('#name_input').val(full_name);
    };

    // Set the private customer name if reloaded
    setNameInputs();

    function setNameInputs(){
        // This splitting is pretty terrible, but will work most of the times
        var names = $('#name_input').val().split(" ");

        var forename = ""
        var surname = ""

        jQuery.each(names, function(index, item) {
            if(index == 0){
                forename = item;
                return true;
            }

            if(index > 1){
                surname += " ";
            }
            surname += item;
        });

        $("#forename_input").val(forename);
        $("#surname_input").val(surname);
    }

    // Set correct fields on first page load
    $("#contact_name_div").hide($('#personal_customer').checked);
    $("#name_input").show($('#personal_customer').checked);
    $("#company_label").show($('#personal_customer').checked)

    $('#personal_customer').click(function() {
        // If personal customer is checked, SHOW these
        $("#contact_name_div").toggle(this.checked);
        $("#title_div").toggle(this.checked);
        $("#organization_div").toggle(this.checked);

        // If personal customer is checked, HIDE these
        $("#name_input").toggle(!this.checked);
        $("#businessid_div").toggle(!this.checked);
        $("#businessid_temp_div").toggle(!this.checked);
        $("#website_div").toggle(!this.checked);
        $("#company_label").toggle(!this.checked);
    });

});