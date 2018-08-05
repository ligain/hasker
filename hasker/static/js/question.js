$(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    var arrow_highlight_class = 'text-primary';

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

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
        var url = "/api/v1/votes/";
        var arrow = $(this);
        var data = {
            "content_type": $(this).data("content-type"),
            "object_id": $(this).data("object-id"),
            "value": $(this).data("value")
        };
        console.log(data);
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
    
    $('.fa-star').on('click', function () {
        // console.log($(this));
        var url = "/api/v1/answers/" + $(this).data("answer-id") + "/";
        var data = {
            "is_right": $(this).data("is-right")
        };
        console.log(data);
        $.ajax({
            type: "patch",
            url: url,
            dataType: 'json',
            data: data,
            xhrFields: {withCredentials: true},
            success: function (data) {
                console.log(data);
            },
            error: function (error) {
                console.log("request to " + url + " failed with an error: ", error);
            }
        })
    })
});