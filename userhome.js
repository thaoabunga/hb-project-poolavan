function searchActivity(results) {
    var activity = results;
    $('#activity').html(activity);
}

function getActivity(){
    $get.('/activity', searchActivity);
}

getActivity();

function viewMyTrips(results) {
    var mytrips = results;
    $('#mytrips').html(results);
}

function getMyTrips(){
    $get.('/mytrips', viewMyTrips);

}

getMyTrips();


function viewAllTrips(results) {
    var alltrips = results;
    $('#alltrips').html(results);
}

function getAllTrips(){
    $get.('/trips', viewAllTrips);

}

getAllTrips();

function viewAllUsers(results) {
    var allusers = results;
    $('#allusers').html(results);
}

function getAllUsers(){
    $get.('/users', viewAllUsers);

}

getAllUsers();

}