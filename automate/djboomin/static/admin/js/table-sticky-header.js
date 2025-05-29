function tableToggleSelect(elt, updateClone) {
    if ($(elt).is(":checked")) {
        if (updateClone) { $('.action-toggle').prop('checked', true); }
        else $('#action-toggle').prop('checked', true);
        $('.action-select').each(function() {
            $(this).prop('checked', true);
            $(this).closest('tr').addClass('selected');
        });
        $('.action-counter').html(_actions_icnt + ' of ' + _actions_icnt + ' selected');
    }
    else {
        if (updateClone) { $('.action-toggle').prop('checked', false); }
        else $('#action-toggle').prop('checked', false);
        $('.action-select').each(function() {
            $(this).prop('checked', false);
            $(this).closest('tr').removeClass('selected');
        });
        $('.action-counter').html('0 of ' + _actions_icnt + ' selected');
    }
}
$(document).ready(function() {
    $(document).on('change', '#action-toggle', function(e) { tableToggleSelect(this, true); });
    $(document).on('change', '.action-toggle', function(e) { tableToggleSelect(this, false); });
    $(document).on('change', '.action-select', function(e) {
        let length = $('.action-select').length;
        let counter = 0;
        $('.action-select').each(function(e) {
            if ($(this).is(":checked")) counter++;
        });
        if (length === counter) {
            $('#action-toggle').prop('checked', true);
            $('.action-toggle').prop('checked', true);
        } else {
            $('#action-toggle').prop('checked', false);
            $('.action-toggle').prop('checked', false);
        }
        $('.action-counter').html(counter + ' of ' + _actions_icnt + ' selected');
    });
});