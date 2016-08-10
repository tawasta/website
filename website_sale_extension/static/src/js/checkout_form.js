$(document).ready(function(){

    $('#personal_customer').click(function() {
        // If personal customer is checked, SHOW these
        $("#contact_label").toggle(this.checked);
        $("#title_div").toggle(this.checked);
        $("#organization_div").toggle(this.checked);

        // If personal customer is checked, HIDE these
        $("#businessid_div").toggle(!this.checked);
        $("#businessid_temp_div").toggle(!this.checked);
        $("#website_div").toggle(!this.checked);
        $("#company_label").toggle(!this.checked);
    });

});