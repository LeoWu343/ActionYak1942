// listening for an event / one-time requests
// coming from the popup
var info = "asdf";
chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
    switch(request.type) {
        case "decrypt-page":
            decryptPage(request.key_guess);
        case "pop_up":
            info = request.info;
        break;
    }
    return true;
});

// send a message to the content script
var decryptPage = function(key_guess) {
	chrome.tabs.getSelected(null, function(tab){
	    chrome.tabs.sendMessage(tab.id, {type: "decrypt-page", key_guess: key_guess});
	});
}

// manipulate the pop up
