$(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var url = "/api/v1/votes/";
    var arrow_highlight_class = 'text-primary';

    function setRating(elem, rating) {
        elem.toggleClass(arrow_highlight_class);
        elem.siblings('.fas').each(function () {
            $(this).removeClass(arrow_highlight_class);
        });
        var counter = elem.siblings(".rating-counter-js").first();
        var current_rating = parseInt(counter.text());
        counter.text(current_rating + rating);
    }

    $('.fa-angle-up, .fa-angle-down').on('click', function () {
        var arrow = $(this);
        var data = {
            "csrfmiddlewaretoken": csrftoken,
            "content_type": $(this).data("content-type"),
            "object_id": $(this).data("object-id"),
            "value": $(this).data("value")
        };

        if (arrow.hasClass(arrow_highlight_class)) {
            data.value = 0;
        }

        $.ajax({
            type: "post",
            url: url,
            dataType: 'json',
            data: data,
            xhrFields: {withCredentials: true},
            success: function (data) {
                if (arrow.hasClass("fa-angle-up") && arrow.hasClass(arrow_highlight_class)) {
                    console.log('undo up');
                    setRating(arrow, -1);
                } else if (arrow.hasClass("fa-angle-down") && arrow.hasClass(arrow_highlight_class)) {
                    console.log('undo down');
                    setRating(arrow, 1);
                } else {
                    setRating(arrow, data.value);
                }
                console.log(data);
            },
            error: function (error) {
                console.log("request to " + url + " failed with an error: ", error);
            }
        })
    });
});