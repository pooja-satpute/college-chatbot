function sendMessage() {
    let inputField = document.getElementById("userInput");
    let message = inputField.value.trim();

    if (message === "") return;

    let chatBox = document.getElementById("chat-box");

    // USER MESSAGE (blue bubble)
    chatBox.innerHTML += `<div class="user-msg">${message}</div>`;

    // Clear input
    inputField.value = "";

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
        // BOT MESSAGE (green bubble)
        chatBox.innerHTML += `<div class="bot-msg">${data.reply}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `<div class="bot-msg" style="background:red;">Server Error</div>`;
    });
}

// Press Enter to send
function handleKey(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
