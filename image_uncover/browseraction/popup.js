window.onload = function() {
        document.getElementById("decrypt").onclick = function() {
            chrome.extension.sendMessage({
                type: "decrypt-page",
                key: document.getElementById("key").value
            });
        }
        document.getElementById("encrypt").onclick = function() {
            var link = document.getElementById("link").value;
            var message = document.getElementById("message").value;
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