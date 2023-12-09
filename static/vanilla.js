// Scroll to the last message
function scrollToLastMessage() {
    var messagesContainer = document.getElementById('messages-container');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

    window.onload = function() {
    scrollToLastMessage();
}

// Save chat as text file
function saveTextFile() {
    var textToWrite = "";
    var messages = document.querySelectorAll("#messages-container .message");
    messages.forEach(function(message) {
        textToWrite += message.innerText + "\n";
    });

    var textBlob = new Blob([textToWrite], {type: 'text/plain'});
    var fileName = "ChatHistory.txt";

    var downloadLink = document.createElement("a");
    downloadLink.download = fileName;
    downloadLink.innerHTML = "Download File";
    if (window.URL != null) {
        downloadLink.href = window.URL.createObjectURL(textBlob);
    } else {
        downloadLink.href = window.URL.createObjectURL(textBlob);
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
    }

    downloadLink.click();
}