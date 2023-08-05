// Author: Jonathan Slenders, City Live

// Usage:
//
//    <div class="show-if-js-enabled" style="display: none;"> becomes   visible if js works </div>
//    <div class="hide-if-js-enabled"                       > becomes invisible if js works </div>

$(function()
{
    // On paginate, apply to pagination container
    function handler(e, containers)
    {
        for (var i in containers)
        {
            // Hide elements with the .hide-if-js-enabled classname
            containers[i].find('.hide-if-js-enabled').each(function() { $(this).hide(); });

            // Show elements with the .show-if-js-enabled classname
            containers[i].find('.show-if-js-enabled').each(function() { $(this).show(); });
        }
    }

    handler(undefined, [ $(document) ]);

    // Initialize again on page/tab loaded
    $(document).bind('paginatorPageReplaced', handler);
    $(document).bind('tabLoaded', handler);
    $(document).bind('xhrLoaded', handler);
});
