window.onload = function() {
        document.getElementById("decrypt").onclick = function() {
            chrome.extension.sendMessage({
                type: "decrypt-page"
            });
        }
        document.getElementById("encrypt").onclick = function() {
            var link = document.getElementById("link").text;
            var message = document.getElementById("message").text;
            sendInfo(link, message);
        }
}

var sendInfo = function(link, message) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:56555/", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            // good
        }
    }
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("goal=encrypt&url_id="+link+"&message="+message);
}