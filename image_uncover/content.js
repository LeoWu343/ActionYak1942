chrome.extension.onMessage.addListener(function(message, sender, sendResponse) {
	switch(message.type) {
		case "decrypt-page":
			var images = document.querySelectorAll("img")
			if(images.length === 0) {
				alert("There are no any images in the page.");
			} else {
				for(var i=0; i<images.length; i++) {
					displayMessage(images[i], message.key);
				}
			}
		break;
	}
});

var displayMessage = function(img, key) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:56555/", true);
	xhr.onreadystatechange = function() {
	    if (xhr.readyState == 4) {
			img.onclick = function() { alert(xhr.responseText); };
	    }
	}
	xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xhr.send("goal=decrypt&url_id="+img.src+"&key="+key);
}