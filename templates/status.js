"use strict";

// function getTrips(e){
// alert("submit clicked");
// showActivity(e);

// }

function searchActivity(results) {
    $('#activity-info').html(results.activity);
}


function createTrips(evt) {
    evt.preventDefault();

    var formValues = {
        "tripName": $("#trip-name-field").serialize(),
        "origin": $("#orgin-field").serialize(),
        "arrival": $("#arrival-field").serialize(),
        "departure_at": $("#departure-field").serialize(),
        "arrival_at": $("#arrival-at-field").serialize(),
        "car_capacity": $("#car_capacity").serialize(),
        "role": $("#role").serialize(),
        "activity": $("#activity").val
    };

    $.post("/createtrip", formValues, resultHandler);
}

// $(function() {
//     $('loginbutton').click(function() {
//         var user = $('#txtUsername').serialize();
//         var pass = $('#txtPassword').serialize();
//         $.ajax({
//             url: '/register',
//             type: 'POST',
//             success: function(response) {
//                 console.log(response);
//             },
//             error: function(error) {
//                 console.log(error);
//             }
//         });
//     });

// // });

// $('#loginbutton').click(function (evt) {
//     $("#userhome").load('/userhome');
// });

