$(function () {
    var ordering = $('h1#title').data('ordering');

    if (ordering === 'new') {
        $('#title-hot').addClass('text-muted');
    } else if (ordering === 'new') {
        $('#title-new').addClass('text-muted');
    }
});