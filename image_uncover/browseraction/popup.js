window.onload = function() {
        document.getElementById("decrypt").onclick = function() {
            chrome.extension.sendMessage({
                type: "decrypt-page",
                key_guess: document.getElementById("key_guess").value
            });
        }
        document.getElementById("encrypt").onclick = function() {
            var link = document.getElementById("link").value;
            var message = document.getElementById("message").value;
            var protection_key = document.getElementById("protection_key").value;
            sendInfo(link, message);
        }
}

var sendInfo = function(link, message, protection_key) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://localhost:56555/", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            document.getElementById("your_link").innerHTML = "<b>Your imgur link!</b><br>"+xhr.responseText;
        }
    }
    xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xhr.send("goal=encrypt&url_id="+link+"&message="+message+"&protection_key="+protection_key);
}