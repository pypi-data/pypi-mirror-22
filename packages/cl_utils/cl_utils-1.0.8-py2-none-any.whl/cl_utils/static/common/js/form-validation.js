/* Author: Jonathan Slenders, City Live */

// Client side form validation script.
// -----------------------------------
// The script reads the meta-information of all the forms
// on this page, if any, and will validate the form when
// submitted. A pop-up dialog is shown when a certain field
// is invalid.

$(function() {
    function ValidationError(label, error_msg, ok_callback)
    {
        this.label = label;
        this.error_msg = error_msg;
        this.ok_callback = ok_callback;
    }

    // For every form
    $('form').each(function() {
        // List of callable validators. (They should throw Error
        // on failure.)
        var validators = [];
        var form = $(this);

        // Create a validator for every meta-information field.
        // (Internet Explorer is namespace aware, and will drop the x: prefix.)
        $(this).find('x\\:form-field-meta, form-field-meta').each(function() {
            var meta = $(this);
            //var field = $('#' + meta.attr('x:ref'));
            var field = form.find('[name=' + meta.attr('x:name') + ']');
            var label = meta.attr('x:label');
            var required = meta.attr('x:required') == 'true';
            var type = meta.attr('x:type');

            function hide_feedback(message){
                // Remove possible serverside errors
                field.siblings('.errorlist').remove();
            }
            function show_feedback(message){
                // Insert own error message
                field.after($('<ul/>').addClass('errorlist').append($('<li/>').text(message)));
            }

            if (field.is('input'))
            {
                function validator()
                {
                    var error = undefined;

                    if (required && ! field.val())
                        error = gettext('This field is required');

                    else if (type == 'email' && ! field.val().match(/.+@.+\..+/))
                        error = gettext('Not a valid e-mail address');

                    hide_feedback();
                    if (error)
                    {
                        show_feedback(error);
                        throw new ValidationError(label, error,
                                function () { field.focus(); return false; });
                    }
                }

                // Validator for field.onchange
                function quick_validate(event)
                {
                    // Ignore tab-key
                    if (event.keyCode != 9)
                    {
                        try { validator(); }
                        catch(validation_error) { }
                    }
                }
                field.change(quick_validate).keyup(quick_validate).blur(quick_validate);

                // Validator for form.submit
                validators.push(validator);
            }
        });

        // Capture onsubmit
        $(this).submit(function() {
            var errors = [];

            // Call all validators
            for (var v in validators)
            {
                try {
                    validators[v]();
                }
                catch(validation_error) {
                    errors.push(validation_error);
                }
            }

            if (errors.length)
            {
                /*
                var msg = $('<div/>');
                msg.append($('<p/>').html(gettext("There was a problem with some values you did or didn't enter.") + "<br/>" + gettext("Please review the following:")));
                var table = $('<table class="error_list" />');
                for (var i in errors)
                {
                    table.append($('<tr/>')
                        .append($('<td class="error_label" />').append($('<strong/>').text(errors[i].label + ': ')))
                        .append($('<td class="error_msg" />').append($('<span/>').text(errors[i].error_msg)))
                        );
                }
                msg.append(table);

                $.mbox(gettext('Please check your input'), msg, {
                        'callback_closed': errors[0].ok_callback,
                        'btn_caption_close': gettext('OK'),
                        'type': DIALOG_OK
                    });
                */
                show_notice(gettext("There was a problem with some values you did or didn't enter.") + " " + gettext("Please correct the errors."), 'error');
                return false;
            }
        });
    });
});
