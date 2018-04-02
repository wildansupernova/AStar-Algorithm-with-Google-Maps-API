var xhr = new XMLHttpRequest();
var url = "/compute";
xhr.open("POST", url, true);
xhr.setRequestHeader("Content-type", "application/json");
xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
        //var json = JSON.parse(xhr.responseText);
        //console.log(json.email + ", " + json.password);
        console.log(xhr.responseText);
    }
};
// var data = JSON.stringify({"email": "hey@mail.com", "password": "101010"});
// xhr.send(data);