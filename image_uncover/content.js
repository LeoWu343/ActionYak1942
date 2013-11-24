chrome.extension.onMessage.addListener(function(message, sender, sendResponse) {
	switch(message.type) {
		case "decrypt-page":
			var images = document.querySelectorAll("img")
			if(images.length === 0) {
				alert("There are no any images in the page.");
			} else {
				for(var i=0; i<images.length; i++) {
					displayMessage(images[i]);
				}
			}
		break;
	}
});

var displayMessage = function(img) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:56555/", true);
	xhr.onstatereadychange = function() {
		img.onClick = function() { alert(xhr.responseText); };
	}
	xhr.send("url_id="+img.src);
}