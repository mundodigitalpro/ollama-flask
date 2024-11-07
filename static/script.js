let conversationHistory = [];

function loadModels() {
    fetch('/models')
        .then(response => response.json())
        .then(data => {
            const modelSelect = document.getElementById('model-select');
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = model;
                modelSelect.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading models:', error));
}

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    const modelSelect = document.getElementById('model-select');
    const message = userInput.value.trim();
    const selectedModel = modelSelect.value;

    if (message) {
        appendMessage('user', message);
        userInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: message, model: selectedModel }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                appendMessage('assistant', `Error: ${data.error}`);
            } else {
                const assistantMessage = document.createElement('div');
                assistantMessage.className = 'message assistant-message';
                chatMessages.appendChild(assistantMessage);
                typeWriter(assistantMessage, data.response);
                
                conversationHistory = data.history;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            appendMessage('assistant', 'Sorry, there was an error processing your request.');
        });
    }
}

function appendMessage(role, content) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${role}-message`);
    messageElement.textContent = content;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function typeWriter(element, text, index = 0) {
    if (index < text.length) {
        element.textContent += text.charAt(index);
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
        setTimeout(() => typeWriter(element, text, index + 1), 20); // Ajusta el 20 para cambiar la velocidad
    }
}

function resetConversation() {
    fetch('/reset', { method: 'POST' })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            conversationHistory = [];
            document.getElementById('chat-messages').innerHTML = '';
            appendMessage('assistant', 'Conversation has been reset. How can I help you?');
        }
    })
    .catch(error => console.error('Error resetting conversation:', error));
}

document.getElementById('user-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

window.onload = loadModels;