// Author: Jonathan Slenders, City Live
//
// Usage
//
// <form ...>
//     <select class="auto-submit" name="type">
//         ...
//     </select><!-- The form will automatically submit when this select box has been changed -->
// </form>


$(function() {
    function init(e, containers)
    {
        for(var i in containers)
            // Find all forms
            containers[i].find('form').each(function() {
                var form = $(this);

                // When in input with auto-submit class has been changed
                form.find('.auto-submit').change(function() {
                    // Submit form
                    form.submit();
                });
            });
    }

    // First time initialisation
    init(undefined, [ $(document) ] );

    // When a tab-page/paginator/xhr has been loaded, initialize again in these containers
    $(document).bind('paginatorPageReplaced', init);
    $(document).bind('tabLoaded', init);
    $(document).bind('xhrLoaded', init);
});
