"use strict";

function userLogin(results) {
    $('#loginbutton').html(results);
}

function showLogin(results) {
    $.get('/userhome'), userLogin);
}

$('#login-button').on('click', showLogin);




function searchActivity(results) {
    $('#search').html(results);
}

function showActivity(results) {
    $.get('/activity'), searchActivity;

$('#')
}

// $(function() {
//     $('loginbutton').click(function() {
//         var user = $('#txtUsername').val();
//         var pass = $('#txtPassword').val();
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

