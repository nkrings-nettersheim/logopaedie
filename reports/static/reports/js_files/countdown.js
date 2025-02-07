
function logout() {
  fetch('/accounts/logout/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRFToken': getCSRFToken(), // Falls CSRF-Schutz aktiv ist
    },
    body: ''
  })
  .then(response => {
    if (response.ok) {
      // Erfolgreich ausgeloggt, Weiterleitung zur Startseite oder Login-Seite
      window.location.href = '/';
    } else {
      console.error('Logout fehlgeschlagen:', response.statusText);
    }
  })
  .catch(error => console.error('Fehler bei der Anfrage:', error));
}

function getCSRFToken() {
  // CSRF-Token aus dem Cookie oder Meta-Tag extrahieren
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


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
        //window.location = "/accounts/logout/";
        // Aufruf der Logout-Funktion, z.B. nach Zeitüberschreitung
        logout();
    }

}

async function makeRequest(url, method, body) {
    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    if (method == 'post') {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]').value
        headers['X-CSRFToken'] = csrf
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await response.json()
}

async function getNumber() {
    const data = await makeRequest("getOpenReportsAjax/", "GET");
    $("#openreports").html(data["openreports"]);
    $("#therapy_break").html(data["therapy_break"]);
}

async function getSessionTimer() {
    const data = await makeRequest("/reports/getsessiontimer/", "GET");
    sessiontimer = await data["sessiontimer"]
    return sessiontimer
}

$(document).ready(function(){
    var logopakt_endTime = new Date();
    //logopakt_endTime = new Date(logopakt_endTime.getTime() + 30*60000);

    getSessionTimer().then(
        function(value) {
            logopakt_endTime = value
        },
        function(error) {
            logopakt_endTime = new Date(logopakt_endTime.getTime() + 60*60000);
        }
    );
    //console.log("Neue Zeit:" + logopakt_endTime)

    if (document.getElementById('openreports') != null) {
        getNumber();
    }


	logopakt_myTimer = setInterval(function() {
	       if (logopakt_endTime <= new Date()) {
	          var t = new Date();
	          t.setSeconds(t.getSeconds() + 2700);
	          logopakt_endTime = t;
           }
	       //console.log(logopakt_endTime)
	       logopakt_makeTimer(logopakt_endTime);
	       }, 1000
       );
});