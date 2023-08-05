{% load i18n %}

$(function() {
    // For each <span class="inline-edit" db:id="823" db:class="UserProfile">...</span>
    $('span.inline-edit').each(function() {
        var span = $(this);
        var edit = false;
        var object_id = $(this).attr('db:id');
        var object_class = $(this).attr('db:class');
        var field = $(this).attr('db:field');

        $(this).css('display', 'block').css('cursor', 'text').css('border', '1px solid transparent').css('min-height', '2ex');
        $(this).mouseover(function(){ if (!edit) $(this).css('border', '1px solid gray') });
        $(this).mouseout(function(){ $(this).css('border', '1px solid transparent') });

        // When clicked on such a field
        span.click(function() {
            if (! edit)
            {
                // Hide border
                $(this).css('border', '1px solid transparent');

                // Show textbox
                var textfield = create_textfield();
                        //textfield.width(span.width());
                textfield.val(span.text());
                textfield.attr('disabled', '');
                span.text('');
                span.append(textfield);
                textfield.focus();
            }
            edit = true;
        });

        // When pressed enter in the textfield
        function create_textfield()
        {
            var textfield = $('<input type="text" />');

            textfield.keypress(function(e) {
                if (e.keyCode == 13)
                {
                    var val = textfield.val();

                    // Disable text field
                    textfield.attr('disabled', 'disabled');
                        // TODO: show loader...

                    // AJAX save
                    $.ajax({
                        type: 'POST',
                        url: '{% url "inline_edit_save" %}',
                        data: { object_id: object_id, object_class: object_class, value: val, field: field },
                        success: function() {
                            // Hide field
                            span.remove(textfield);
                            span.text(val);
                            edit = false;
                        },
                        error: function() {
                            alert ("{% trans "Saving error" %}");
                            textfield.attr('disabled', '');
                        }
                    });
                }
            });
            return textfield;
        }

    });
});
