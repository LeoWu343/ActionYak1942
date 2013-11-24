chrome.extension.onMessage.addListener(function(message, sender, sendResponse) {
	switch(message.type) {
		case "decrypt-page":
			var images = document.querySelectorAll("img")
			if(images.length === 0) {
				alert("There are no any images in the page.");
			} else {
				for(var i=0; i<images.length; i++) {
					if (images[i].src != "") {
						displayMessage(images[i]);
					}
				}
			}
		break;
	}
});

var displayMessage = function(img) {
	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:56555/", true);
	xhr.onreadystatechange = function() {
	    if (xhr.readyState == 4) {
			response = JSON.parse(xhr.responseText);
			if (response.has_message) {
				if (response.correct_key) {
					message = response.message;
					img.onclick = function() { alert(message); };
				} else {
					img.onclick = function() { alert("WRONG KEY"); };
				}
			} else {
				img.onclick = function() { alert('No hidden message!'); };
			}
	    }
	}
	xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xhr.send("url_id=" + img.src + "&key=12345678"); //key should not be hardcoded
}
