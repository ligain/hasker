$(function () {
    $('.fa-angle-up').on('click', function () {
        var form = $(this).parent('form');
        var value_field = '<input name="value" type="hidden" value="1">';
        form.append(value_field);
        form.submit();
    });
    $('.fa-angle-down').on('click', function () {
        var form = $(this).parent('form');
        var value_field = '<input name="value" type="hidden" value="-1">';
        form.append(value_field);
        form.submit();
    })
});