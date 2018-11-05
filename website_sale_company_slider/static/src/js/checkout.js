odoo.define('website_sale_company_slider.checkout', function (require) {
    "use strict";

    $(function() {

        function showFields() {
            var is_company = $('#is_company').is(':checked');
            if (is_company === true) {
                $('#is_company_info').removeClass('hidden');
                $('#not_is_company_info').addClass('hidden');
                $("label[for='company_name']").removeClass('label-optional');
                $("label[for='vat']").removeClass('label-optional');
                $('#is_company').attr("checked", "checked");
            } else {
                $('#is_company_info').addClass('hidden');
                $('#not_is_company_info').removeClass('hidden');
                $("label[for='company_name']").addClass('label-optional');
                $("label[for='vat']").addClass('label-optional');
                $('#is_company').removeAttr("checked");
            }
        }

        $('#is_company').click(function() {
            showFields();
        });

        $('.oe_website_sale .a-submit, #comment .a-submit').off('click').on('click', function (event) {
            if (!event.isDefaultPrevented() && !$(this).is(".disabled")) {
                // If country is Finland and VAT is inserted, make business id
                var form = $(this).closest('form');
                var vat = $(form).find("input[name='vat']").val();
                var country_id = $('#country_id').val();
                if (vat && country_id == 71) {
                    var parsed = vat.replace(/[^0-9]/g, '');
                    var business_id = parsed.substr(0, 7) + '-' + parsed.substr(7, 1);
                    $(form).append('<input type="hidden" name="business_id" value="' + business_id + '"/>');
                }
                $(this).closest('form').submit();
            }
            if ($(this).hasClass('a-submit-disable')){
                $(this).addClass("disabled");
            }
            if ($(this).hasClass('a-submit-loading')){
                var loading = '<span class="fa fa-cog fa-spin"/>';
                var fa_span = $(this).find('span[class*="fa"]');
                if (fa_span.length){
                    fa_span.replaceWith(loading);
                }
                else{
                    $(this).append(loading);
                }
            }
        });
    });
});
