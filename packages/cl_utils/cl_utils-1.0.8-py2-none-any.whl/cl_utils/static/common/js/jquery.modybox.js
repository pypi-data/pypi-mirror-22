/*
 * Modybox
 * Version 0.1 alpha (19/02/2010)
 * Requires: jQuery 1.3+
*/

(function($) {
    $.fn.fixPNG = function() {
        return this.each(function () {
            var image = $(this).css('backgroundImage');

            if (image.match(/^url\(["']?(.*\.png)["']?\)$/i)) {
                image = RegExp.$1;
                $(this).css({
                    'backgroundImage': 'none',
                    'filter': "progid:DXImageTransform.Microsoft.AlphaImageLoader(enabled=true, sizingMethod=" + ($(this).css('backgroundRepeat') == 'no-repeat' ? 'crop' : 'scale') + ", src='" + image + "')"
                }).each(function () {
                    var position = $(this).css('position');
                    if (position != 'absolute' && position != 'relative')
                        $(this).css('position', 'relative');
                });
            }
        });
    };
    
    var isIE = ($.browser.msie && parseInt($.browser.version.substr(0,1)) < 8);
    var imageLoader = new Image();
    var prevent_closing = false;
    DIALOG_OK = 'ok';
    DIALOG_CLOSE = 'close';
    DIALOG_YES_NO = 'yes_no';
    DIALOG_YES_NO_CANCEL = 'yes_no_cancel';
    
    /*
     * modybox class
     */
    $.modybox = function(title, data, settings) {
        if (settings)
            settings = $.extend(false, $.modybox.settings, settings);  
        else
            settings = $.extend(false, $.modybox.settings);
        
        $.modybox.loading(settings);
        $.modybox.show(settings);
        $.modybox.show_data(title, data, DIALOG_CLOSE, settings);
        $.fn.modybox.fix_box(true);
    };
    
    $.extend($.modybox, {
        settings: {
            overlay_show       : true,
            overlay_opacity    : 0.3,
            loading_image      : 'img/modybox/loading.gif',
            close_image        : 'img/modybox/close.gif',
            media_url          : '/media/',
            hide_on_click      : true,
            show_title         : true,
            show_footer        : true,
            auto_height        : false,
            imageRegExp        : /\.(jpg|gif|png|bmp|jpeg)(.*)?$/i,
            type               : DIALOG_OK,
            dialog_title       : '',
            dialog_content     : '',
            callback_closing   : null,
            callback_closed    : null,
            callback_yes       : null,
            callback_no        : null,
            btn_caption_yes    : 'Yes',
            btn_caption_no     : 'No',
            btn_caption_cancel : 'Cancel',
            btn_caption_ok     : 'Ok',
            btn_caption_close  : 'Close'
        },
        
        loading: function(settings) {
            prevent_closing = true;
            if (typeof settings == 'undefined') settings = $.modybox.settings;
        
            init();
            
            // clear content
            $('#modybox_wrap .modybox_body').empty();
            
            // add loading image
            $('#modybox_wrap .modybox_body').html('<div class="modybox_loading"><img src="' + settings.media_url + settings.loading_image + '" alt="" /></div>');
            if (settings.hide_on_click)
                $('#modybox_overlay').bind('click', function() {$.modybox.close(settings)});
            $('.modybox_loading').bind('click', function() {$.modybox.close(settings)});
            
            // esc close
            $(document).bind('keydown.modybox', function(e) {
                if (e.keyCode == 27) {
                    $.modybox.close();
                }
                return true;
            });
            
            // resize binding
            $(window).bind('resize', $.fn.modybox.scroll);
            
            if (isIE) {
                $('embed, object, select').css('visibility', 'hidden');
            }
            prevent_closing = false;
        },
        
        show: function(settings) { 
            prevent_closing = true;
            if (typeof settings == 'undefined') settings = $.modybox.settings;
              
            // show overlay if need
            if (settings.overlay_show) {
                $('#modybox_overlay').css({
                    'opacity': settings.overlay_opacity
                }).show();
            }
            
            // show box
            $.fn.modybox.scroll();
            $('#modybox_wrap').show();
            prevent_closing = false;
        },
        
        show_data: function(title, content, type, settings) {
            prevent_closing = true;
            if (typeof settings == 'undefined') settings = $.modybox.settings;
            
            if (type == null)
                type = DIALOG_OK;
        
            $('#modybox_wrap .modybox_body').html('');
            if (settings.show_title)
                $('#modybox_wrap .modybox_body').append('<div class="modybox_title"></div>');
        
            $('#modybox_wrap .modybox_body').append('<div class="modybox_content"></div>');            
            if (settings.show_footer)
                $('#modybox_wrap .modybox_body').append('<div class="modybox_footer"></div>');
                
            $('#modybox_wrap .modybox_title').append(title);
            $('#modybox_wrap .modybox_content').append(content);
        
            if (settings.show_footer) {
                $('#modybox_wrap .modybox_footer').append($.fn.modybox.get_footer(type, settings));
                $.modybox.connect_handlers(type, settings);
            }
            
            $('#modybox_wrap .modybox_loading').remove();
            
            $.fn.modybox.scroll();
            
            $('#modybox_wrap').children().fadeIn(10);
            $('#modybox_wrap').css({
                'left': $(window).width() / 2 - ($('#modybox_wrap table').width() / 2)
            });
            prevent_closing = false;
        },
        
        show_image: function(image_src, type, settings) {
            var pos = $.fn.modybox.getViewport();
            
            var r = Math.min(Math.min(pos[0] - 50, imageLoader.width) / imageLoader.width,
                            Math.min(pos[1] - 120, imageLoader.height) / imageLoader.height);

            var width = Math.round(r * imageLoader.width);
            var height = Math.round(r * imageLoader.height);
            
            $.modybox.show_data('', '<img src="'+image_src+'" width="'+width+'" height="'+height+'" alt="" />', type, settings)
        },
        
        close: function(settings) {
            if (prevent_closing)
            {
                return false;
            }
            
            if (typeof settings == 'undefined') settings = $.modybox.settings;
            
            if ($.isFunction(settings.callback_closing))
            {
                settings.callback_closing($.modybox.element);
            }
            
            // do cleanup stuff
            $(document).unbind('keydown.modybox');
            $('#modybox_wrap').fadeOut(10, function() {
                $('#modybox_overlay').fadeOut('fast', function() {
                    $('#modybox_wrap .modybox_body').empty();
                    $('#modybox_wrap').attr('style', '').hide();
                    $('#modybox_wrap #modybox_table').attr('style', '');
                });
            });
            
            if (settings.hide_on_click)
                $('#modybox_overlay').unbind('click');
            $('.modybox_loading').unbind('click');
            $('#modybox_wrap .modybox_loading').remove();
            $(window).unbind('resize');
            
            if (isIE) {
                $('embed, object, select').css('visibility', 'visible');
            }
            
            if ($.isFunction(settings.callback_closed))
            {
                settings.callback_closed($.modybox.element);
            }
            
            return false;
        },
        
        connect_handlers: function(type, settings) {    
            switch (type) {
                    case DIALOG_YES_NO:
                        if ($.isFunction(settings.callback_yes))
                        {
                            $('#modybox_wrap .modybox_footer .btn_yes').click(function(){
                                settings.callback_yes($.modybox.element);
                                $.modybox.close(settings);
                            });
                        }
                        if ($.isFunction(settings.callback_no))
                        {
                            $('#modybox_wrap .modybox_footer .btn_no').click(function(){
                                settings.callback_no($.modybox.element);
                                $.modybox.close(settings);
                            });
                        }
                        else
                        {
                            $('#modybox_wrap .modybox_footer .btn_no').click(function(){
                                $.modybox.close(settings);
                            });
                        }
                        break;
                    case DIALOG_YES_NO_CANCEL:
                        if ($.isFunction(settings.callback_yes))
                        {
                            $('#modybox_wrap .modybox_footer .btn_yes').click(function(){
                                settings.callback_yes($.modybox.element);
                                $.modybox.close(settings);
                            });
                        }
                        else if ($.isFunction(settings.callback_no))
                        {
                            $('#modybox_wrap .modybox_footer .btn_no').click(function(){
                                settings.callback_no($.modybox.element);
                                $.modybox.close(settings);
                            });
                        }
                        else
                        {
                            $('#modybox_wrap .modybox_footer .btn_cancel').click(function(){
                                $.modybox.close(settings);
                            });
                        }
                        break;
                    case DIALOG_CLOSE:
                    case DIALOG_OK:
                    default:
                        $('#modybox_wrap .modybox_footer .btn_ok').click(function(){
                            $.modybox.close(settings);
                        });
                        break;
            }
        }
    });
    
    /*
     * end modybox class
     */
     
    $.fn.modybox = function(settings) {
        init();
        
        function _initialize(){
            $.modybox.element = $(this);
            $.fn.modybox.start(settings);
            return false;
        };
        
        return this.unbind('click').click(_initialize);
    };
    
    function init() {
        if ($.modybox.settings.initialised) return true;
        else $.modybox.settings.initialised = true;
        $.fn.modybox.build();
    };
    
    $.fn.modybox.getViewport = function() {
        return [$(window).width(), $(window).height(), $(document).scrollLeft(), $(document).scrollTop()];
    };
    
    $.fn.modybox.start = function(settings) {
        /*
         * types:
         *  div #id
         *  image
         *  url
         */
         
        if (settings)
            settings = $.extend(false, $.modybox.settings, settings);  
        else
            settings = $.extend(false, $.modybox.settings);
        
        $.modybox.loading(settings);
        $.modybox.show(settings);
        
        elem = $.modybox.element;
        elem_href = elem.attr("href");
        
        if (settings.dialog_title != '')
            elem_title = settings.dialog_title;
        else if (!elem.attr("title"))
            elem_title = '';
        else
            elem_title = elem.attr("title");
        
        if (settings.dialog_content != '')
        {
            $.modybox.show_data(elem_title, settings.dialog_content, settings.type, settings);
            $.fn.modybox.fix_box(settings.auto_height);
        }
        else
        {
            // div
            if (elem_href.match(/#/))
            {
                var url    = window.location.href.split('#')[0];
                var target = elem_href.replace(url,'');
                
                $.modybox.show_data(elem_title, $(target).clone(), settings.type, settings);
                $.fn.modybox.fix_box(settings.auto_height);
            }
            // image
            else if (elem_href.match(settings.imageRegExp))
            {
                settings.show_title = false;
                settings.type = DIALOG_CLOSE;
            
                imageLoader = new Image();
                imageLoader.src = elem_href;
                
                imageLoader.onerror = function() {
                    $.fn.modybox.error();
                };
                
                imageLoader.onload = function() {
                    imageLoader.onerror = null;
                    imageLoader.onload = null;
                    $.modybox.show_image(imageLoader.src, settings.type, settings);
                    $.fn.modybox.fix_box(true);
                };
                imageLoader.src = elem_href;
            }
            /*else if (elem_href.match('iframe') || elem.hasClass('iframe')) 
            {
                $.modybox.show_data(elem_title, '<iframe id="modybox_iframe" name="modybox_iframe" onload="$.fn.modybox.show_iframe()" width="100%" frameborder="0" hspace="0" src="' + elem_href + '"></iframe>', settings.type, settings);
                $.fn.modybox.fix_box(settings.auto_height);
            }*/
            // url
            else
            {
                $.ajax({
                    url:    elem_href,
                    //data:   ,
                    error:  $.fn.modybox.error,
                    success: function(data, textStatus, XMLHttpRequest) {
                        $.modybox.show_data(elem_title, data, settings.type, settings);
                        $.fn.modybox.fix_box(settings.auto_height);
                    }
                });
            }
        }
    };
    
    $.fn.modybox.error = function() {
        $.modybox.show_data('Error', '<p>The requested data could not be loaded. Please try again.</p>', DIALOG_OK);
        $.fn.modybox.fix_box(true);
    };
    
    $.fn.modybox.get_footer = function(type, settings) {
        if (typeof settings == 'undefined') settings = $.modybox.settings;
        var footer_html = '';
    
        switch (type) {
                case DIALOG_YES_NO:
                    footer_html  = '<p>';
                    footer_html += '    <input type="button" class="btn_yes" value="' + settings.btn_caption_yes + '" />';
                    footer_html += '    <input type="button" class="btn_no" value="' + settings.btn_caption_no + '" />';
                    footer_html += '</p>';
                    break;
                case DIALOG_YES_NO_CANCEL:
                    footer_html  = '<p>';
                    footer_html += '    <input type="button" class="btn_yes" value="' + settings.btn_caption_yes + '" />';
                    footer_html += '    <input type="button" class="btn_no" value="' + settings.btn_caption_no + '" />';
                    footer_html += '    <input type="button" class="btn_cancel" value="' + settings.btn_caption_cancel + '" />';
                    footer_html += '</p>';
                    break;
                case DIALOG_CLOSE:
                    footer_html  = '<p>';
                    footer_html += '    <input type="button" class="btn_ok" value="' + settings.btn_caption_close + '" />';
                    footer_html += '</p>';
                    break;
                case DIALOG_OK:
                default:
                    footer_html  = '<p>';
                    footer_html += '    <input type="button" class="btn_ok" value="' + settings.btn_caption_ok + '" />';
                    footer_html += '</p>';
                    break;
        }
        
        return footer_html;
    };

    $.fn.modybox.show_iframe = function() {    
        var iframe = $('#modybox_wrap #modybox_iframe');
        var innerDoc = (iframe.get(0).contentDocument) ? iframe.get(0).contentDocument : iframe.get(0).contentWindow.document;
        
        iframe.css({
            'height': innerDoc.body.scrollHeight + 35
        });
        
        $.fn.modybox.fix_box(true);
    };
    
    $.fn.modybox.scroll = function() {    
        var pos = $.fn.modybox.getViewport();        

        $("#modybox_wrap").css({
            'left'    : (($("#modybox_wrap").width() + 40) > pos[0] ? pos[2] : pos[2] + Math.round((pos[0] - $("#modybox_wrap").width() - 40) / 2)),
            'top'     : (($("#modybox_wrap").height() + 50) > pos[1] ? pos[3] : (pos[3] + Math.round((pos[1] - $("#modybox_wrap").height() - 50) / 2)))
        });
    };
    
    $.fn.modybox.fix_box = function(skip_height) {
        var pos = $.fn.modybox.getViewport();
        
        // content width
        var width = $("#modybox_wrap .modybox_body").width() + 20;
        if ($("#modybox_wrap .modybox_body #modybox_iframe").length > 0) {
            width = $("#modybox_wrap .modybox_body #modybox_iframe").width() + 20;
        }
        
        if (width < 500)
            width = 500;
        else if (width > pos[0])
            width = pos[0] * 0.80;
            
        $('#modybox_wrap').css({
            'width':width+'px' /*,
            'height':height+'px'*/
        });
        
        $('#modybox_wrap #modybox_table').css({
            'width':'100%'
        });
        
        if (typeof skip_height == undefined || !skip_height) {
            $('#modybox_wrap .modybox_content').css({
                'height':'300px'
            });
        }
        
        height = $('#modybox_wrap .modybox_body').height();
        if (height > pos[1]) 
        {
            height = pos[1] * 0.80;
            
            if ($("#modybox_wrap .modybox_body #modybox_iframe").length > 0) {
                $("#modybox_wrap .modybox_body #modybox_iframe").css({
                    'height': height + 'px'
                });
            } else {
                $('#modybox_wrap .modybox_body').css({
                    'height': height + 'px'
                });
            }
        }
        
        $.fn.modybox.scroll();
    };
    
    $.fn.modybox.build = function () {
        var html = '';
        
        html += '<div id="modybox_overlay" style="display:none;"></div>';
        html += '<div id="modybox_wrap" style="display:none;">';
        html += '<div id="modybox" style="display:none;">';
        html += '   <table id="modybox_table">';
        html += '       <tr>';
        html += '           <td class="modybox_tl" />';
        html += '           <td class="modybox_t" />';
        html += '           <td class="modybox_tr" />';
        html += '       </tr>';
        html += '       <tr>';
        html += '           <td class="modybox_l" />';
        html += '           <td class="modybox_body">';
        html += '               <div class="modybox_title"></div>';
        html += '               <div class="modybox_content"></div>';
        html += '               <div class="modybox_footer"></div>';
        html += '           </td>';
        html += '           <td class="modybox_r" />';
        html += '       </tr>';
        html += '       <tr>';
        html += '           <td class="modybox_bl" />';
        html += '           <td class="modybox_b" />';
        html += '           <td class="modybox_br" />';
        html += '       </tr>';
        html += '   </table>';
        html += '</div>';
        html += '</div>';
        
        $(html).appendTo("body");
        
        if (isIE) {
            $('.modybox_tl, .modybox_t, .modybox_tr, .modybox_l, .modybox_r, .modybox_bl, .modybox_b, .modybox_br').fixPNG();
        }
    };
}) (jQuery);
