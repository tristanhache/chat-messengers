document.addEventListener("DOMContentLoaded", function() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var username = "{{ username }}"; // Get the username from the rendered template

    // Function to add a new message to the chat
    function addMessage(user, message) {
        var messages = document.getElementById('messages');
        var li = document.createElement('li');
        li.innerHTML = '<b>' + user + '</b>: ' + message;
        messages.appendChild(li);

        // Store the message in local storage
        var chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        chatHistory.push({ user: user, message: message });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    }

    // Retrieve and display chat history from local storage
    function displayChatHistory() {
        var chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
        chatHistory.forEach(function(entry) {
            addMessage(entry.user, entry.message);
        });
    }

    // Handle sending messages
    var messageForm = document.getElementById('message-form');
    if (messageForm) {
        messageForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var messageInput = document.getElementById('message');
            var message = messageInput.value;
            if (message.trim() !== '') {
                // Display the message immediately
                addMessage(username, message);
                // Send the message to the server
                socket.emit('message', { message: message });
                messageInput.value = '';
            }
        });
    }

    // Handle receiving messages from the server
    socket.on('message', function(data) {
        addMessage(data.user, data.message);
    });

    // Initialize by displaying chat history from local storage
    displayChatHistory();
});
