function ucFirst(string, element) {
    var focusControl = document.forms[0].elements[element];
    string = string.substring(0, 1).toUpperCase() + string.substring(1);
    focusControl.value = string
}

function CheckDate(elementValue, element) {
    var focusControl = document.forms[0].elements[element];
    var new_value = elementValue.replace(/,/g, ".");
    var new_value = new_value.replace(/\//g, ".");
    focusControl.value = new_value;
}


function makeTimer(endTime) {

    endTime = (Date.parse(endTime) / 1000);

    var now = new Date();
    now = (Date.parse(now) / 1000);

    var timeLeft = endTime - now - 5;

    var days = Math.floor(timeLeft / 86400);
    var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
    var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
    var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

    //if (days < "10") { days = "0" + days; }
    //if (hours < "10") { hours = "0" + hours; }
    if (minutes < "10") { minutes = "0" + minutes; }
    if (seconds < "10") { seconds = "0" + seconds; }

    $("#minutes").html(minutes);
    $("#seconds").html(seconds);

    if (timeLeft < 0) {
        clearInterval(myTimer);
        window.location = "/accounts/logout/";
    }

}

$(document).ready(function(){
    var endTime = new Date();
    var data = new Date();
    $.get("/reports/getSessionTimer", function(data, status){
      endTime = data;
    });

    if (document.getElementById('openreports') != null) {
      $.get("/reports/getOpenReports", function(data, status){
        $("#openreports").html(data);
      });
    }

	myTimer = setInterval(function() { makeTimer(endTime); }, 1000);
});