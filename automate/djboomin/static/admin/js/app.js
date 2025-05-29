if (typeof String.prototype.startsWith != 'function') {
    String.prototype.startsWith = function (str){
        return this.indexOf(str) === 0;
    };
}
$(document).ready(function() {
    $('body').delegate('a', 'click', function(e) {
        if ($(this).hasClass('subnav-dropdown')) {
            $(this).parent().find('ul').slideToggle(100);
            $(this).toggleClass('active');
            e.preventDefault();
        } else if ($(this).attr('href') == '#') {
            e.preventDefault();
        }
    });

    $('.actions').each(function() {
        $(this).find('select').addClass('form-control').addClass('input-sm');
    });

    $('p.file-upload').each(function() {
        var currentFileLink = $($(this).find('a')[0]);
        if (!currentFileLink) return;

        var fileURL = currentFileLink.attr('href');
        var fileField = $(this);

        var ajaxHEADRequest = $.ajax({
            url: fileURL,
            type: 'HEAD',
            async: true,
            success: function(data) {
                var contentType = ajaxHEADRequest.getResponseHeader('Content-Type');
                if (contentType.startsWith('image')) {
                    var img = $('<div></div>').css({
                        backgroundImage: 'url(' + fileURL + ')',
                        backgroundSize: 'contain',
                        backgroundPosition: 'center center',
                        backgroundRepeat: 'no-repeat',
                        position: 'relative',
                        width: 60,
                        height: 60,
                        float: 'left',
                        marginRight: 10
                    });
                    fileField.prepend(img);
                } else {
                    var ext = fileURL.split('.').pop();
                    if (ext.length > 5) {
                        ext = '_blank';
                    }

                    var img = $('<div></div>').css({
                        backgroundImage: 'url(/static/admin/images/icons/80px/' + ext + '.png)',
                        backgroundSize: 'contain',
                        backgroundPosition: 'center center',
                        backgroundRepeat: 'no-repeat',
                        width: 60,
                        height: 60,
                        float: 'left',
                        marginRight: 10
                    }).on('error', function() {
                        if ($(this).attr('haserror')) {
                            $(this).remove();
                            return;
                        }
                        $(this).attr('haserror', '1');
                        $(this).css('background-image', 'url(/static/admin/images/icons/80px/_blank.png)');
                    });
                    fileField.prepend(img);
                }
            }
        });
    });
    $("select[multiple]").each(function() {
        var _input = $(this);
        if (!$(this).closest('.form-row').hasClass('empty-form')) {
            $(this).chosen({width: '100%'});
        }
        var selectAllButton = $('<a href="#">Select All</a>');
        var deselectAllButton = $('<a href="#">Deselect All</a>');

        selectAllButton.click(function(e) {
            e.preventDefault();
            _input.children().prop('selected', true);
            _input.trigger("chosen:updated");
        });

        deselectAllButton.click(function(e) {
            e.preventDefault();
            _input.children().prop('selected', false);
            _input.trigger("chosen:updated");
        });

        $(this).parent().append(selectAllButton).append('&nbsp;|&nbsp;').append(deselectAllButton);
    });
    $('p.help-block:contains("Hold down")').hide();
    jQuery('body').on('rowadded', function(e, row) {
        jQuery(row.find("select[multiple]")).chosen({width: '100%'});
        $(row).find("textarea.ckeditor-field").ckeditor();
    })
});
$(window).load(function() {
    $('textarea.ckeditor-field').each(function() {
        if($(this).closest('.empty-form').length === 0) {
            $(this).ckeditor();
        }
    });
});
