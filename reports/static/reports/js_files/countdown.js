
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


function logopakt_makeTimer(logopakt_endTime) {

    logopakt_endTime = (Date.parse(logopakt_endTime) / 1000);
    //console.log('logopakt_endTime: ' + logopakt_endTime)

    var logopakt_now = new Date();
    logopakt_now = (Date.parse(logopakt_now) / 1000);
    //console.log('logopakt_now: ' + logopakt_now)

    var logopakt_timeLeft = logopakt_endTime - logopakt_now -5;
    //console.log('logopakt_timeLeft: ' + logopakt_timeLeft)

    var days = Math.floor(logopakt_timeLeft / 86400);
    var hours = Math.floor((logopakt_timeLeft - (days * 86400)) / 3600);
    var minutes = Math.floor((logopakt_timeLeft - (days * 86400) - (hours * 3600 )) / 60);
    var seconds = Math.floor((logopakt_timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));

    //if (days < "10") { days = "0" + days; }
    //if (hours < "10") { hours = "0" + hours; }
    if (minutes < "10") { minutes = "0" + minutes; }
    if (seconds < "10") { seconds = "0" + seconds; }

    $("#minutes").html(minutes);
    $("#seconds").html(seconds);

    if (logopakt_timeLeft < 0) {
        clearInterval(logopakt_myTimer);
        window.location = "/accounts/logout/";
    }

}

$(document).ready(function(){
    var logopakt_endTime = new Date();
    logopakt_endTime = new Date(logopakt_endTime.getTime() + 45*60000);
    //console.log('logopakt_endTime0: ' + logopakt_endTime)
    //dies ist eine Test
    //$.get("/reports/getSessionTimer", function(data, status){
      //console.log('getSessionTimer ' +  data)
    //  logopakt_endTime = data;
    //  console.log('logopakt_endTime1: ' +  logopakt_endTime)
    //});

    $.ajax({
        type: 'GET',
        url: "/reports/getsessiontimer/",
        success: function (response) {
                //console.log(response)
                let logopakt_endTime = response.sessiontimer;
                console.log("Inhalt: " + logopakt_endTime)
            },
            error: function (response) {
                console.log(response);
            }
        })

    if (document.getElementById('openreports') != null) {
      //console.log('getOpenReports')
      $.get("/reports/getOpenReports", function(data, status){
                  result = data.split('|')
                  $("#openreports").html(result[0]);
                  $("#therapy_break").html(result[1]);
             });
    }

	logopakt_myTimer = setInterval(function() {
	       //console.log('Aktuelle Zeit    : ' + new Date())
	       console.log('logopakt_endTime: ' + logopakt_endTime)

	       if (logopakt_endTime <= new Date()) {
	          var t = new Date();
	          console.log("logopakt_endTime nicht definirt")
	          t.setSeconds(t.getSeconds() + 2700);
	          logopakt_endTime = t;
	       }
	       logopakt_makeTimer(logopakt_endTime);
	       }, 1000
       );

});