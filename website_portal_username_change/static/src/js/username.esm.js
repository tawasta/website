/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";
import Dialog from "@web/legacy/js/core/dialog";
import {_t} from "@web/core/l10n/translation";

var ChangeUsernameModal = publicWidget.Widget.extend({
    selector: '.o_portal_wrap',
    events: {
        'click #changeUsernameModal': '_onClickChangeUsernameButton',
    },

    start: function () {
        this._super.apply(this, arguments);
        $(document).on("submit", "#change_username_form", this._onFormSubmit.bind(this));
    },

    _onClickChangeUsernameButton: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();
        
        jsonrpc("/my/change_username/modal", {}).then(function (modalContent) {
            const $modal = $(modalContent);
            $modal.find('.modal-body > div').removeClass('container');
            $modal.appendTo(document.body);
            const modalBS = new Modal($modal[0], { backdrop: 'static', keyboard: false });
            modalBS.show();

            $modal.on('click', '.btn-close', function () {
                $modal.remove();
            });
            $modal.on('hidden.bs.modal', function () {
                $modal.remove();
            });
        }).catch(function (err) {
            console.error("Failed to load modal content", err);
        });
    },

    _onFormSubmit: function (ev) {
        ev.preventDefault();
        ev.stopPropagation();

        const $form = $(ev.currentTarget);
        const actionUrl = $form.attr('action');
        const formData = new FormData($form[0]);
        this._showLoadingScreen();
        $.ajax({
            url: actionUrl,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                const jsonResponse = JSON.parse(response);
                if (jsonResponse.error) {
                    this._showErrorMessage(jsonResponse.msg);
                } else {
                    this._showSuccessMessage(jsonResponse.success);
                    $form.closest('.modal').modal('hide');
                }
            },
            error: (err) => {
                this._showErrorMessage("An unexpected error occurred.");
            },
            complete: () => {
                this._hideLoadingScreen();
            },
        });
    },

    _showSuccessMessage: function (message) {
        new Dialog(this, {
            title: _t("Success"),
            size: "medium",
            $content: $("<div/>").html(message),
            buttons: [
                {
                    text: _t("OK"),
                    close: true,
                    click: function () {
                        window.location.href = "/web/login";
                    },
                },
            ],
        }).open();
    },

    _showLoadingScreen: function () {
        const loadingMessage = `
            <div id="loading-screen" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #fff;
                font-size: 20px;">
                <div>
                    <div class="spinner-border text-light" role="status"></div>
                    <p>Loading, please wait...</p>
                </div>
            </div>`;
        $('body').append(loadingMessage);
    },

    _hideLoadingScreen: function () {
        $('#loading-screen').remove();
    },

    _showErrorMessage: function (message) {
        new Dialog(this, {
            title: _t("Error"),
            size: "medium",
            $content: $("<div/>").html(message),
            buttons: [
                {
                    text: _t("OK"),
                    close: true,
                },
            ],
        }).open();
    },

});

publicWidget.registry.ChangeUsernameModal = ChangeUsernameModal;
