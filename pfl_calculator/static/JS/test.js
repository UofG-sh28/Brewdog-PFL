

var response;

$(document).ready(() => {
    response = document.getElementById("response");
});


const host = "127.0.0.1:8000"


function getDatabaseData(){
    const requestURL = new URL("http://" + host + "/database_api")
    console.log("http://" + host + "/database_api")
    const xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const json = JSON.parse(this.responseText);

            console.log(JSON.stringify(json));
            response.innerText = JSON.stringify(json);
        }
    }

    // set parameters
    requestURL.searchParams.set("id", "value");
    xhttp.open("GET", requestURL, false);
    xhttp.send();
}