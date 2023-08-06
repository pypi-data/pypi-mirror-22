/**
 * Created by javier on 26-04-17.
 */

$(function() {
    console.log( "ready!" );

    $.ajax(
        {
            type: "get",
            url: "/pictures/photo/blob/",
            data: {
                'photo_name': '184834294',
                'token': '8b2a8e46e40279606bd227990ce6ce33de96d8ff',
                'refresh': true
            }
        })
        .done(function(response) {
            console.log(response);
        })
        .fail(function() {
            alert( "error" );
        })
        .always(function() {
            console.log("complete");
        });


});


