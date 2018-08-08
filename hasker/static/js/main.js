$(function () {
    var ordering = $('h2#title').data('ordering');

    if (ordering === 'new') {
        $('#title-hot').addClass('text-muted');
    } else if (ordering === 'hot') {
        $('#title-new').addClass('text-muted');
    }
});