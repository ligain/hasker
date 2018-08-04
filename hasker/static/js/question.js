$(function () {
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
    $('.fa-angle-up').on('click', function () {
        var data = {
            "csrfmiddlewaretoken": csrftoken,
            "content_type": $(this).data("content-type"),
            "object_id": $(this).data("object-id"),
            "value": -11
            // "value": $(this).data("value")
        };
        // console.log($(this).data("content-type"));
        // console.log($(this).data("object-id"));
        // console.log($(this).data("value"));
        // console.log(csrftoken);

        // $.post("/api/v1/votes/", data, function (data) {
        //     console.log(data);
        // }).fail(function (error) {
        //     console.log("request to /api/v1/votes/ failed with an error: ", error);
        // });

        $.ajax({
            type: "post",
            url: "/api/v1/votes/",
            dataType: 'json',
            data: data,
            xhrFields: { withCredentials: true },
            success: function (data) {
                console.log(data);
            },
            error: function (error) {
                console.log("request to /api/v1/votes/ failed with an error: ", error);
            }
        })

    });
    $('.fa-angle-down').on('click', function (e) {
        // var form = $(this).parent('form');
        // var value_field = '<input name="value" type="hidden" value="-1">';
        // form.append(value_field);
        // form.submit();
    })
});