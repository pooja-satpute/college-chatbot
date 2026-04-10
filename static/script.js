function sendMessage() {
    let inputField = document.getElementById("userInput");
    let message = inputField.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chat-box");

    // Show user message
    chatBox.innerHTML += `<p><b>You:</b> ${message}</p>`;

    // Send to backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p><b>Bot:</b> ${data.reply}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `<p style="color:red;">Error: Server not responding</p>`;
    });

    inputField.value = "";
}

// Press Enter to send
function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
