
/************************************************************
 *
 * tailbone.mobile.js
 *
 * Global logic for mobile app
 *
 ************************************************************/


$(function() {

    // must init header/footer toolbars since ours are "external"
    $('[data-role="header"], [data-role="footer"]').toolbar({theme: 'a'});
});


$(document).on('pagecontainerchange', function(event, ui) {

    // in some cases (i.e. when no user is logged in) we may want the (external)
    // header toolbar button to change between pages.  here's how we do that.
    // note however that we do this *always* even when not technically needed
    var link = $('[data-role="header"] a');
    var newlink = ui.toPage.find('.replacement-header a');
    link.text(newlink.text());
    link.attr('href', newlink.attr('href'));
    link.removeClass('ui-icon-home ui-icon-user');
    link.addClass(newlink.attr('class'));
});


$(document).on('pagecreate', function() {

    // setup any autocomplete fields
    $('.field.autocomplete').mobileautocomplete();

});


/**
 * Automatically set focus to certain fields, on various pages
 * TODO: this should accept selector params instead of hard-coding..?
 */
function setfocus() {
    var el = null;
    var queries = [
        '#username',
        '#new-purchasing-batch-vendor-text',
        // '.receiving-upc-search',
    ];
    $.each(queries, function(i, query) {
        el = $(query);
        if (el.is(':visible')) {
            el.focus();
            return false;
        }
    });
}


$(document).on('pageshow', function() {

    setfocus();

    // TODO: seems like this should be better somehow...
    // remove all flash messages after 2.5 seconds
    window.setTimeout(function() { $('.flash, .error').remove(); }, 2500);

});


// vendor validation for new purchasing batch
$(document).on('click', 'form[name="new-purchasing-batch"] input[type="submit"]', function() {
    var $form = $(this).parents('form');
    if (! $form.find('[name="vendor"]').val()) {
        alert("Please select a vendor");
        $form.find('[name="new-purchasing-batch-vendor-text"]').focus();
        return false;
    }
});

// submit new purchasing batch form on Purchase click
$(document).on('click', 'form[name="new-purchasing-batch"] [data-role="listview"] a', function() {
    var $form = $(this).parents('form');
    var $field = $form.find('[name="purchase"]');
    var uuid = $(this).parents('li').data('uuid');
    $field.val(uuid);
    $form.submit();
    return false;
});


// disable datasync restart button when clicked
$(document).on('click', '#datasync-restart', function() {
    $(this).button('disable');
});



// handle Enter press for receiving UPC lookup
$(document).on('keydown', '.receiving-upc-search', function(event) {
    if (event.which == 13) {
        $.mobile.navigate($(this).data('url') + '?upc=' + $(this).val());
    }
});


// handle numeric buttons for receiving
// $(document).on('click', '#receiving-quantity-keypad-thingy .ui-btn', function() {
$(document).on('click', '#receiving-quantity-keypad-thingy .keypad-button', function() {
    var quantity = $('.receiving-quantity');
    var value = quantity.text();
    var key = $(this).text();
    var changed = $('#receiving-quantity-keypad-thingy').data('changed');
    if (key == 'Del') {
        if (value.length == 1) {
            quantity.text('0');
        } else {
            quantity.text(value.substring(0, value.length - 1));
        }
        changed = true;
    } else if (key == '.') {
        if (value.indexOf('.') == -1) {
            if (changed) {
                quantity.text(value + '.');
            } else {
                quantity.text('0.');
                changed = true;
            }
        }
    } else {
        if (value == '0') {
            quantity.text(key);
            changed = true;
        } else if (changed) {
            quantity.text(value + key);
        } else {
            quantity.text(key);
            changed = true;
        }
    }
    if (changed) {
        $('#receiving-quantity-keypad-thingy').data('changed', true);
    }
});


// handle receiving action buttons
$(document).on('click', '.receiving-actions button', function() {
    var action = $(this).data('action');
    var form = $('form.receiving-update');
    var uom = form.find('[name="receiving-uom"]').val();
    var qty = form.find('.receiving-quantity').text();
    if (action == 'add' || action == 'subtract') {
        if (qty != '0') {
            if (action == 'subtract') {
                qty = '-' + qty;
            }
            if (uom == 'CS') {
                form.find('[name="cases"]').val(qty);
            } else { // units
                form.find('[name="units"]').val(qty);
            }
            form.submit();
        }
    }
});
