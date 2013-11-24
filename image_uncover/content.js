chrome.extension.onMessage.addListener(function(message, sender, sendResponse) {
	switch(message.type) {
		case "decrypt-page":
			var images = document.querySelectorAll("img")
			if(images.length === 0) {
				alert("There are no any images in the page.");
			} else {
				for(var i=0; i<images.length; i++) {
					if (images[i].src != "") {
							displayMessage(images[i], message.key_guess);
						}
				}
			}
		break;
	}
});

// TODO: notify user when done processing
var displayMessage = function(img, key_guess) {
	var xhr2 = new XMLHttpRequest();
	xhr2.open("POST", "http://localhost:56555/", true);
	xhr2.onreadystatechange = function() {
	    if (xhr2.readyState == 4) {
			response = JSON.parse(xhr2.responseText);
			if (response.has_message) {
				if (response.correct_key) {
					message = response.message;
					div = document.createElement("div");
					div2 = document.createElement("div");
					div.setAttribute("style","background-image: url(" + img.src + "); background-size: contain; border: 1px solid black; height: "+img.clientHeight+"px; width: "+img.clientWidth+"px;");
					div2.setAttribute("style","background-color: #f0f0f0; width:100%; text-align:center; opacity:0.8;");
					div2.innerHTML = "<font color='black' size='5'><p><b>"+message+"</b></p></font>";
					img.parentNode.replaceChild(div, img);
					div.appendChild(div2);
					//img.onclick = function() { alert(message); };
				} else {
					img.onclick = function() { alert("WRONG KEY"); };
				}
			} else {
				img.onclick = function() { alert('No hidden message!'); };
			}
	    }
	}
	xhr2.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xhr2.send("goal=decrypt&url_id="+img.src+"&key_guess="+key_guess);
}
