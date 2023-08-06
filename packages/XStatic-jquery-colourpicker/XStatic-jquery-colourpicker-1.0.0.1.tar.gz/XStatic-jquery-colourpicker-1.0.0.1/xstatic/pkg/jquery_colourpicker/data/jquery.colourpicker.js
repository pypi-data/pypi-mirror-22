/* adapted from http://andreaslagerkvist.com/jquery/colour-picker/ */

jQuery.fn.colourPicker = function (conf) {
    // Config for plug
    var config = jQuery.extend({
        id:            'jquery-colour-picker',    // id of colour-picker container
        inputBG:    true,                    // Whether to change the input's background to the selected colour's
        speed:        500                    // Speed of dialogue-animation
    }, conf);

    // Inverts a hex-colour
    var hexInvert = function (hex) {
        var r = parseInt(hex.substr(0, 2), 16);
        var g = parseInt(hex.substr(2, 2), 16);
        var b = parseInt(hex.substr(4, 2), 16);

        return 0.212671 * r + 0.715160 * g + 0.072169 * b < 128 ? 'ffffff' : '000000'
    };

    // Add the colour-picker dialogue if not added
    var colourPicker = jQuery('#' + config.id);

    if (!colourPicker.length) {
        colourPicker = jQuery('<div id="' + config.id + '"></div>').appendTo(document.body).hide();

        // Remove the colour-picker if you click outside it (on body)
        jQuery(document.body).click(function(event) {
            if (!(jQuery(event.target).is('#' + config.id) || jQuery(event.target).parents('#' + config.id).length)) {
                colourPicker.hide(config.speed);
            }
        });
    }

    // For every select passed to the plug-in
    return this.each(function () {
        // Insert icon and input
        var select    = jQuery(this);
        var icon    = jQuery('<a href="#">...</a>').insertAfter(select);
        var input    = jQuery('<input type="text" name="' + select.attr('name') + '" value="' + select.val() + '" size="7" />').insertAfter(select);
        var loc        = '';

        // Build a list of colours based on the colours in the select
        jQuery('option', select).each(function () {
            var option    = jQuery(this);
            var hex        = option.val();
            var title    = option.text();

            loc += '<li><a href="#" title="' 
                    + title 
                    + '" rel="' 
                    + hex 
                    + '" style="background: #' 
                    + hex 
                    + '; colour: ' 
                    + hexInvert(hex) 
                    + ';">' 
                    + title 
                    + '</a></li>';
        });

        // Remove select
        select.remove();

        // If user wants to, change the input's BG to reflect the newly selected colour
        if (config.inputBG) {
            input.change(function () {
                input.css({background: '#' + input.val(), color: '#' + hexInvert(input.val())});
            });

            input.change();
        }

        // When you click the icon
        icon.click(function () {
            // Show the colour-picker next to the icon and fill it with the colours in the select that used to be there
            var iconPos    = icon.offset();

            colourPicker.html('<ul>' + loc + '</ul>').css({
                position: 'absolute', 
                left: iconPos.left + 'px', 
                top: iconPos.top + 'px'
            }).show(config.speed);

            // When you click a colour in the colour-picker
            jQuery('a', colourPicker).click(function () {
                // The hex is stored in the link's rel-attribute
                var hex = jQuery(this).attr('rel');

                input.val(hex);

                // If user wants to, change the input's BG to reflect the newly selected colour
                if (config.inputBG) {
                    input.css({background: '#' + hex, color: '#' + hexInvert(hex)});
                }

                // Trigger change-event on input
                input.change();

                // Hide the colour-picker and return false
                colourPicker.hide(config.speed);

                return false;
            });

            return false;
        });
    });
};

$(function() {
  jQuery('select.colour-picker').colourPicker();
});
