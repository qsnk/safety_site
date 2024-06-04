$(document).ready(function() {
    $('#clean_inputs').click(function() {
        $('input[type="date"]').each(function() {
           $(this).val('');
        });
        $('input[type="time"]').each(function() {
           $(this).val('');
        });
        $(':checkbox').each(function() {
            this.checked = false;
        });
    });
});
