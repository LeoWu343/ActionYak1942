// omnibox
chrome.omnibox.onInputChanged.addListener(function(text, suggest) {
	suggest([
	  {content: "decrypt-page", description: "Decrypt the page"}
	]);
});
chrome.omnibox.onInputEntered.addListener(function(text) {
	if(text == "decrypt-page") decryptPage();
});

// listening for an event / one-time requests
// coming from the popup
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    switch(request.type) {
        case "decrypt-page":
            decryptPage();
        break;
    }
    return true;
});

// listening for an event / long-lived connections
// coming from devtools
chrome.extension.onConnect.addListener(function (port) {
    port.onMessage.addListener(function (message) {
       	switch(port.name) {
			case "color-divs-port":
				decryptPage();
			break;
		}
    });
});

// send a message to the content script
var decryptPage = function() {
	chrome.tabs.getSelected(null, function(tab){
	    chrome.tabs.sendMessage(tab.id, {type: "decrypt-page"});
	});
}